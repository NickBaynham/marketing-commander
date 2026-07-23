"""AIP approval, versions, and export API tests (Phase 7, Increment 7.2).

Full-stack against a scratch database migrated to head: eligibility
gating, immutable version creation, superseding, approval records, the
read/export endpoints, and the API half of the two-layer immutability
guarantee (no mutation route on versions). The DB-trigger half is proven
in test_aip_version_immutability.py.

Traceability: REQ-010, REQ-013, REQ-014, REQ-015, REQ-016; AC-006,
AC-007; BR-004, BR-005, BR-006, BR-020; DEC-02, DEC-03; API-12..14; D7-6.
"""

import asyncio
import json
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

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
    yield client
    client.close()
    asyncio.run(engine.dispose())
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


def eligible_artist(client: TestClient, name: str) -> tuple[str, int]:
    """Create an artist and save a minimal-valid (approval-eligible)
    draft. Returns (artist_id, current draft version token)."""
    client.post("/api/v1/workspace", json={"name": "CYR3NT Workspace"})
    artist_id = client.post("/api/v1/artists", json={"name": name}).json()["id"]
    saved = client.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": 1, "sections": fixture("aip_minimal_valid")},
    )
    assert saved.status_code == 200, saved.text
    return artist_id, saved.json()["version_token"]


def test_approve_creates_immutable_version_and_approval(api):
    artist_id, token = eligible_artist(api, "Approve One")
    response = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": token},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["version_number"] == 1
    assert body["version_label"] == "1.0"
    assert body["status"] == "approved"
    assert body["artist_id"] == artist_id
    assert body["approved_by"] == "local-owner"  # DEC-03 non-null actor
    assert body["approved_at"] is not None


def test_approve_blocked_when_ineligible_names_sections(api):
    api.post("/api/v1/workspace", json={"name": "CYR3NT Workspace"})
    artist_id = api.post(
        "/api/v1/artists", json={"name": "Ineligible"}
    ).json()["id"]
    response = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": 1},
    )
    assert response.status_code == 422, response.text
    error = response.json()["error"]
    fields = {d["field"] for d in error["details"]}
    # All nine required sections are empty on a fresh draft (AC-006).
    assert len(fields) == 9
    assert "sections.core_identity" in fields
    # No version was created.
    versions = api.get(f"/api/v1/artists/{artist_id}/aip/versions").json()
    assert versions == []


def test_approve_stale_draft_token_conflicts(api):
    artist_id, token = eligible_artist(api, "Stale Approve")
    response = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": token - 1},
    )
    assert response.status_code == 409, response.text


def test_superseding_marks_prior_version_superseded(api):
    artist_id, token = eligible_artist(api, "Supersede")
    first = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": token},
    ).json()

    # Edit the draft again, then approve a second version.
    resaved = api.put(
        f"/api/v1/artists/{artist_id}/aip",
        json={"expected_version": token, "sections": fixture("aip_minimal_valid")},
    ).json()
    second = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": resaved["version_token"]},
    ).json()

    assert second["version_number"] == 2
    assert second["version_label"] == "2.0"
    assert second["status"] == "approved"

    # The prior version is now derived-superseded; still readable, label
    # unchanged (REQ-015: prior record unchanged).
    prior = api.get(f"/api/v1/aip-versions/{first['id']}").json()
    assert prior["version_number"] == 1
    assert prior["version_label"] == "1.0"
    assert prior["status"] == "superseded"


def test_list_versions_reports_status_and_approver(api):
    artist_id, token = eligible_artist(api, "List Versions")
    api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": token},
    )
    versions = api.get(f"/api/v1/artists/{artist_id}/aip/versions").json()
    assert len(versions) == 1
    assert versions[0]["status"] == "approved"
    assert versions[0]["approved_by"] == "local-owner"


def test_get_unknown_version_404(api):
    response = api.get(f"/api/v1/aip-versions/{uuid.uuid4()}")
    assert response.status_code == 404


def test_export_renders_markdown_snapshot(api):
    artist_id, token = eligible_artist(api, "Export Me")
    version = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": token},
    ).json()
    export = api.get(f"/api/v1/aip-versions/{version['id']}/export")
    assert export.status_code == 200, export.text
    markdown = export.json()["markdown"]
    assert markdown.startswith("---")  # YAML front matter
    assert "Export Me" in markdown
    assert "Core identity" in markdown


def test_versions_expose_no_mutation_route(api):
    """API half of REQ-014: an approved version has no update or delete
    route (405), so no supported API path can mutate it."""
    artist_id, token = eligible_artist(api, "No Mutation")
    version = api.post(
        f"/api/v1/artists/{artist_id}/aip/approve",
        json={"expected_version": token},
    ).json()
    assert api.put(f"/api/v1/aip-versions/{version['id']}", json={}).status_code == 405
    assert api.delete(f"/api/v1/aip-versions/{version['id']}").status_code == 405
