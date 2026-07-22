"""AipService unit tests with fake collaborators (no I/O).

Traceability: REQ-006, REQ-007, REQ-045; AC-004, AC-005, AC-008;
BR-019, BR-020; Phase 6 Increment 6.2.
"""

import asyncio
import json
import uuid
from pathlib import Path

import pytest

from app.domain.aip import AipSections
from app.domain.aip_service import AipService
from app.exceptions import NotFound, StaleVersion, ValidationFailed

FIXTURES = Path(__file__).parent / "fixtures"


def sections(name: str) -> AipSections:
    return AipSections.model_validate(
        json.loads((FIXTURES / f"{name}.json").read_text())
    )


class FakeProfile:
    def __init__(self, artist_id, version_token=1, sections_doc=None):
        self.artist_id = artist_id
        self.version_token = version_token
        self.sections = sections_doc or {}


class FakeAipRepo:
    def __init__(self, profile, name="CYR3NT"):
        self._profile = profile
        self._name = name
        self.saved = False
        self.raise_on_save = None

    async def get(self, artist_id):
        if self._profile is None or self._profile.artist_id != artist_id:
            return None
        return self._profile

    async def artist_name(self, artist_id):
        return self._name

    async def save(self, profile):
        if self.raise_on_save is not None:
            raise self.raise_on_save
        self.saved = True
        return profile


class FakeAudit:
    def __init__(self):
        self.records = []

    async def record(self, **kwargs):
        self.records.append(kwargs)


def run(coro):
    return asyncio.run(coro)


def make_service(profile, name="CYR3NT"):
    repo = FakeAipRepo(profile, name)
    audit = FakeAudit()
    return AipService(aip=repo, audit=audit, actor_id="local-owner"), repo, audit


def test_get_draft_missing_profile_raises_notfound():
    service, _, _ = make_service(None)
    with pytest.raises(NotFound):
        run(service.get_draft(uuid.uuid4()))


def test_get_draft_reports_derived_state():
    artist_id = uuid.uuid4()
    profile = FakeProfile(artist_id, sections_doc=sections("aip_minimal_valid").model_dump(mode="json"))
    service, _, _ = make_service(profile)
    state = run(service.get_draft(artist_id))
    assert state.completeness == 1.0
    assert state.approval_eligible is True
    assert state.incomplete_required_sections == []
    assert state.version_token == 1


def test_save_persists_audits_and_returns_state():
    artist_id = uuid.uuid4()
    profile = FakeProfile(artist_id)
    service, repo, audit = make_service(profile)
    state = run(service.save_draft(artist_id, 1, sections("aip_minimal_valid")))
    assert repo.saved is True
    assert state.approval_eligible is True
    assert profile.sections["core_identity"]["status"] == "ready_for_review"
    assert audit.records[0]["action"] == "aip.saved"
    assert audit.records[0]["entity_type"] == "artist_identity_profile"
    assert audit.records[0]["actor_id"] == "local-owner"


def test_save_stale_precheck_raises_before_touching_repo():
    artist_id = uuid.uuid4()
    profile = FakeProfile(artist_id, version_token=5)
    service, repo, audit = make_service(profile)
    with pytest.raises(StaleVersion):
        run(service.save_draft(artist_id, 1, sections("aip_minimal_valid")))
    assert repo.saved is False
    assert audit.records == []


def test_save_total_size_violation_is_validation_failed():
    artist_id = uuid.uuid4()
    profile = FakeProfile(artist_id)
    service, repo, _ = make_service(profile)
    oversized = AipSections.model_validate(
        {
            name: {"content": "x" * 20_000, "status": "draft", "sources": []}
            for name in AipSections.model_fields
        }
    )
    with pytest.raises(ValidationFailed) as caught:
        run(service.save_draft(artist_id, 1, oversized))
    assert caught.value.rule == "max_total_length"
    assert repo.saved is False


def test_save_maps_concurrent_stale_from_repo():
    artist_id = uuid.uuid4()
    profile = FakeProfile(artist_id)
    service, repo, _ = make_service(profile)
    repo.raise_on_save = StaleVersion("lost race")
    with pytest.raises(StaleVersion):
        run(service.save_draft(artist_id, 1, sections("aip_minimal_valid")))


def test_preview_renders_markdown_with_artist_name():
    artist_id = uuid.uuid4()
    profile = FakeProfile(artist_id, sections_doc=sections("aip_minimal_valid").model_dump(mode="json"))
    service, _, _ = make_service(profile, name="CYR3NT")
    markdown = run(service.preview(artist_id))
    assert markdown.startswith("---\n")
    assert 'artist: "CYR3NT"' in markdown
    assert "## Core identity" in markdown
