"""Workspace and artist API tests (Phase 5, Increment 5.2).

Full-stack API tests: TestClient with the session dependency bound to a
scratch database migrated to head, so validation shapes, concurrency,
lifecycle rules, and audit records are asserted against the real schema.

Traceability: REQ-001 (idempotent workspace), REQ-003/AC-002 (creation),
AC-003 (422 field+rule shape), BR-019 (409 stale), BR-014 (archived
read-only, AC-025), BR-015/REQ-051 (confirmed deletion), BR-020/REQ-040
(audit records with non-null actor).
"""

import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models import AuditRecord
from tests.conftest import compose_stack_reachable
from tests.test_domain_schema import make_scratch_db
from tests.test_migrations import admin_execute

pytestmark = pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)


@pytest.fixture(scope="module")
def api(request):
    from app.db import get_session
    from app.main import create_app

    name, dsn = make_scratch_db()
    # NullPool: TestClient serves each request on its own anyio loop, so
    # pooled asyncpg connections would be bound to a dead loop.
    engine = create_async_engine(dsn, poolclass=NullPool)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_session():
        async with maker() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    client = TestClient(app)
    yield client, dsn
    client.close()
    asyncio.run(engine.dispose())
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


def test_workspace_create_is_idempotent(api):
    client, _ = api
    first = client.post("/api/v1/workspace", json={"name": "CYR3NT Workspace"})
    assert first.status_code == 200 and first.json()["created"] is True
    second = client.post("/api/v1/workspace", json={"name": "Another Name"})
    body = second.json()
    assert second.status_code == 200 and body["created"] is False
    assert body["id"] == first.json()["id"]
    assert client.get("/api/v1/workspace").json()["name"] == "CYR3NT Workspace"


def test_artist_lifecycle_via_api(api):
    client, dsn = api
    created = client.post(
        "/api/v1/artists", json={"name": "  CYR3NT  ", "genre": "melodic techno"}
    )
    assert created.status_code == 201, created.text
    artist = created.json()
    assert artist["name"] == "CYR3NT"  # trimmed per D5-1
    assert artist["state"] == "active" and artist["version_token"] == 1
    artist_id = artist["id"]

    # AC-003: duplicate (case-insensitive) names field and rule.
    duplicate = client.post("/api/v1/artists", json={"name": "cyr3nt"})
    assert duplicate.status_code == 422
    detail = duplicate.json()["error"]["details"][0]
    assert detail["field"] == "name" and detail["rule"] == "unique_per_workspace"

    # AC-003: shape validation names the field.
    invalid = client.post("/api/v1/artists", json={"name": ""})
    assert invalid.status_code == 422
    assert any(
        "name" in d["field"] for d in invalid.json()["error"]["details"]
    )

    # Read paths.
    assert any(
        a["id"] == artist_id for a in client.get("/api/v1/artists").json()
    )
    assert client.get(f"/api/v1/artists/{artist_id}").status_code == 200

    # BR-019: stale version is a 409 with the envelope.
    stale = client.patch(
        f"/api/v1/artists/{artist_id}",
        json={"expected_version": 99, "summary": "won't apply"},
    )
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "conflict"

    updated = client.patch(
        f"/api/v1/artists/{artist_id}",
        json={"expected_version": 1, "summary": "Berlin-leaning melodic techno"},
    )
    assert updated.status_code == 200 and updated.json()["version_token"] == 2

    # BR-014 / AC-025: archived blocks mutation; restore lifts it.
    archived = client.post(
        f"/api/v1/artists/{artist_id}/archive", json={"expected_version": 2}
    )
    assert archived.status_code == 200 and archived.json()["state"] == "archived"
    blocked = client.patch(
        f"/api/v1/artists/{artist_id}",
        json={"expected_version": 3, "summary": "nope"},
    )
    assert blocked.status_code == 409
    restored = client.post(
        f"/api/v1/artists/{artist_id}/restore", json={"expected_version": 3}
    )
    assert restored.status_code == 200 and restored.json()["state"] == "active"

    # BR-015 / REQ-051: deletion requires confirmation and names the loss.
    unconfirmed = client.delete(f"/api/v1/artists/{artist_id}")
    assert unconfirmed.status_code == 422
    assert unconfirmed.json()["error"]["details"][0]["field"] == "confirm"
    deleted = client.delete(f"/api/v1/artists/{artist_id}?confirm=true")
    assert deleted.status_code == 200
    assert deleted.json()["removed"]["artist"] == "CYR3NT"
    assert client.get(f"/api/v1/artists/{artist_id}").status_code == 404

    # BR-020 / REQ-040: every state change wrote an audit record with the
    # seeded actor.
    async def audit_actions() -> list[tuple[str, str]]:
        engine = create_async_engine(dsn)
        try:
            async with async_sessionmaker(engine)() as session:
                result = await session.execute(
                    select(AuditRecord.action, AuditRecord.actor_id).where(
                        AuditRecord.entity_id == artist_id
                    )
                )
                return list(result.all())
        finally:
            await engine.dispose()

    records = asyncio.run(audit_actions())
    actions = {action for action, _ in records}
    assert {
        "artist.created",
        "artist.updated",
        "artist.archived",
        "artist.restored",
        "artist.deleted",
    } <= actions
    assert all(actor == "local-owner" for _, actor in records)
