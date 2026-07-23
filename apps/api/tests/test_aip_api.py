"""AIP API tests against the real schema (Phase 6, Increment 6.2).

Full-stack: TestClient with the session bound to a scratch database
migrated to head, so persistence, optimistic concurrency, size limits,
the preview contract, and audit records are asserted for real.

Traceability: REQ-006, REQ-007, REQ-012, REQ-045; AC-004, AC-005,
AC-008; BR-019, BR-020; Phase 6 Increment 6.2.
"""

import asyncio
import json
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models import ArtistIdentityProfile, AuditRecord
from tests.conftest import compose_stack_reachable
from tests.test_domain_schema import make_scratch_db
from tests.test_migrations import admin_execute

pytestmark = pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name: str) -> dict:
    return json.loads((FIXTURES / f"{name}.json").read_text())


@pytest.fixture(scope="module")
def api():
    from app.db import get_session
    from app.main import create_app

    name, dsn = make_scratch_db()
    engine = create_async_engine(dsn, poolclass=NullPool)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_session():
        async with maker() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    from tests.conftest import authenticate_as
    authenticate_as(app)
    client = TestClient(app)
    yield client, dsn
    client.close()
    asyncio.run(engine.dispose())
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


def make_artist(client: TestClient, name: str) -> str:
    client.post("/api/v1/workspace", json={"name": "CYR3NT Workspace"})
    created = client.post("/api/v1/artists", json={"name": name})
    assert created.status_code == 201, created.text
    return created.json()["id"]


def test_new_draft_is_empty_and_ineligible(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Empty")
    response = client.get(f"/api/v1/artists/{artist_id}/aip")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["version_token"] == 1
    assert body["completeness"] == 0.0
    assert body["approval_eligible"] is False
    assert len(body["incomplete_required_sections"]) == 9


def test_unknown_artist_returns_404(api):
    client, _ = api
    response = client.get(f"/api/v1/artists/{uuid.uuid4()}/aip")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_save_persists_and_resumes(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Persist")
    saved = client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_minimal_valid")},
    )
    assert saved.status_code == 200, saved.text
    body = saved.json()
    assert body["version_token"] == 2
    assert body["approval_eligible"] is True

    # Resume: a fresh GET returns the persisted sections and derived state.
    resumed = client.get(f"/api/v1/artists/{artist_id}/aip").json()
    assert resumed["version_token"] == 2
    assert resumed["completeness"] == 1.0
    assert (
        resumed["sections"]["core_identity"]["status"] == "ready_for_review"
    )


def test_stale_save_is_409(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Stale")
    client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_minimal_valid")},
    )
    # Second save still using the now-stale version 1.
    stale = client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_incomplete")},
    )
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "conflict"


def test_per_section_oversize_is_422_naming_the_section(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Oversize")
    payload = fixture("aip_minimal_valid")
    payload["core_identity"]["content"] = "x" * 20_001
    response = client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": payload},
    )
    assert response.status_code == 422
    fields = [d["field"] for d in response.json()["error"]["details"]]
    assert any("core_identity" in field for field in fields)


def test_total_oversize_is_422(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Total")
    from app.domain.aip import ALL_SECTIONS

    # Each section within its 20k cap, but 12 * 20k = 240k > 200k total.
    payload = {
        name: {"content": "x" * 20_000, "status": "draft", "sources": []}
        for name in ALL_SECTIONS
    }
    response = client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": payload},
    )
    assert response.status_code == 422
    detail = response.json()["error"]["details"][0]
    assert detail["rule"] == "max_total_length"


def test_preview_contract(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Preview")
    client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_minimal_valid")},
    )
    response = client.get(f"/api/v1/artists/{artist_id}/aip/preview")
    assert response.status_code == 200
    markdown = response.json()["markdown"]
    assert markdown.startswith("---\n")
    assert markdown.count("\n## ") == 12  # one heading per section
    assert "## Core identity" in markdown
    assert 'artist: "E2E Preview"' in markdown


def test_preview_keeps_adversarial_text_inert(api):
    client, _ = api
    artist_id = make_artist(client, "E2E Adversarial")
    client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_adversarial")},
    )
    markdown = client.get(
        f"/api/v1/artists/{artist_id}/aip/preview"
    ).json()["markdown"]
    front_matter = markdown.split("---\n")[1]
    assert "<script>" not in front_matter
    assert "Ignore all previous instructions" in markdown  # data, under a heading


def test_save_writes_audit_with_correlation(api):
    client, dsn = api
    artist_id = make_artist(client, "E2E Audit")
    client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_minimal_valid")},
    )

    async def rows():
        engine = create_async_engine(dsn)
        try:
            async with async_sessionmaker(engine)() as session:
                result = await session.execute(
                    select(AuditRecord.actor_id, AuditRecord.correlation_id).where(
                        AuditRecord.action == "aip.saved",
                        AuditRecord.entity_id == artist_id,
                    )
                )
                return list(result.all())
        finally:
            await engine.dispose()

    records = asyncio.run(rows())
    assert records
    assert all(actor == "local-owner" for actor, _ in records)
    assert all(correlation for _, correlation in records)


def test_true_concurrent_race_is_caught_by_conditioned_update(api):
    """B1 lesson for the AIP: two sessions load the same draft at the
    same version and both save; the loser's version-conditioned UPDATE
    matches no row and raises StaleVersion — the precheck alone could not
    prevent this under READ COMMITTED."""
    client, dsn = api
    artist_id = make_artist(client, "E2E Race")

    async def race():
        from app.exceptions import StaleVersion
        from app.repositories.aip import AipRepository

        engine = create_async_engine(dsn, poolclass=NullPool)
        maker = async_sessionmaker(engine, expire_on_commit=False)
        try:
            aid = uuid.UUID(artist_id)
            async with maker() as s1, maker() as s2:
                p1 = await AipRepository(s1).get(aid)
                p2 = await AipRepository(s2).get(aid)
                p1.sections = {"core_identity": {"content": "first writer wins here"}}
                await AipRepository(s1).save(p1)
                await s1.commit()
                p2.sections = {"core_identity": {"content": "second writer loses"}}
                with pytest.raises(StaleVersion):
                    await AipRepository(s2).save(p2)
        finally:
            await engine.dispose()

    asyncio.run(race())
