"""Authorization enforcement API tests (Phase 8, Increment 8.3).

Full-stack against a scratch database with the identity and role
resolution NOT overridden: real logins as members of each role hit
protected routes, proving the role-action matrix (D8-4) is enforced at
the API — allow, 403 on insufficient role, 401 unauthenticated, and 403
for a non-member (deny by default, the enforceable BR-001 boundary).

Traceability: AC-029; REQ-054, REQ-055; BR-001; DEC-03; D8-4.
"""

import asyncio
import uuid

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

PASSWORD = "correct-horse-role-pw"
ARTIST_ID = uuid.UUID("019f9000-0000-7000-8000-00000000a001")


@pytest.fixture(scope="module")
def api():
    from app.db import get_session
    from app.identity import IDENTITY_SOURCE
    from app.main import create_app
    from app.models import (
        Artist,
        ArtistIdentityProfile,
        User,
        Workspace,
        WorkspaceMembership,
    )
    from app.security import hash_password

    name, dsn = make_scratch_db()
    engine = create_async_engine(dsn, poolclass=NullPool)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    roles = [
        ("owner-user", "owner"),
        ("editor-user", "editor"),
        ("reviewer-user", "reviewer"),
        ("viewer-user", "viewer"),
        ("outsider-user", None),  # authenticated but not a member
    ]

    async def seed():
        async with maker() as session:
            # Users first: the workspace FK references the owner.
            for user_id, _ in roles:
                session.add(
                    User(
                        id=user_id,
                        display_name=user_id,
                        identity_source=IDENTITY_SOURCE,
                        password_hash=hash_password(PASSWORD),
                    )
                )
            await session.flush()
            ws = Workspace(name="Authz Workspace", created_by="owner-user")
            session.add(ws)
            await session.flush()
            for user_id, role in roles:
                if role is not None:
                    session.add(
                        WorkspaceMembership(
                            user_id=user_id,
                            workspace_id=ws.id,
                            role=role,
                            granted_by="owner-user",
                        )
                    )
            artist = Artist(id=ARTIST_ID, workspace_id=ws.id, name="Authz Artist")
            session.add(artist)
            await session.flush()
            session.add(
                ArtistIdentityProfile(artist_id=artist.id, workspace_id=ws.id)
            )
            await session.commit()

    asyncio.run(seed())

    async def override_session():
        async with maker() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    client = TestClient(app)
    yield client
    client.close()
    asyncio.run(engine.dispose())
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


@pytest.fixture
def as_role(api):
    def _login(user_id: str) -> TestClient:
        api.cookies.clear()
        response = api.post(
            "/api/v1/auth/login",
            json={"username": user_id, "password": PASSWORD},
        )
        assert response.status_code == 200, response.text
        return api

    return _login


def create_artist_body(name: str) -> dict:
    return {"name": name}


# View is permitted to every member (matrix row 1).


@pytest.mark.parametrize(
    "user_id", ["owner-user", "editor-user", "reviewer-user", "viewer-user"]
)
def test_view_allowed_for_every_member(as_role, user_id):
    client = as_role(user_id)
    assert client.get(f"/api/v1/artists/{ARTIST_ID}").status_code == 200


# Create artist: authoring roles allowed, others 403.


def test_editor_can_create_artist(as_role):
    client = as_role("editor-user")
    response = client.post("/api/v1/artists", json=create_artist_body("E2E Authz A"))
    assert response.status_code == 201


@pytest.mark.parametrize("user_id", ["reviewer-user", "viewer-user"])
def test_non_authoring_roles_cannot_create_artist(as_role, user_id):
    client = as_role(user_id)
    response = client.post("/api/v1/artists", json=create_artist_body("nope"))
    assert response.status_code == 403


# Approval separation: reviewer may approve (passes authz → reaches the
# eligibility check, 422 on the empty draft), editor may not (403).


def test_reviewer_passes_authz_on_approve(as_role):
    client = as_role("reviewer-user")
    response = client.post(
        f"/api/v1/artists/{ARTIST_ID}/aip/approve",
        json={"expected_version": 1},
    )
    # Not 403: authorization allowed the action; the empty draft is then
    # blocked by the DEC-02 eligibility gate.
    assert response.status_code == 422


def test_editor_denied_on_approve(as_role):
    client = as_role("editor-user")
    response = client.post(
        f"/api/v1/artists/{ARTIST_ID}/aip/approve",
        json={"expected_version": 1},
    )
    assert response.status_code == 403


# Delete artist: owner allowed past authz, editor denied.


def test_editor_cannot_delete_artist(as_role):
    client = as_role("editor-user")
    response = client.request(
        "DELETE", f"/api/v1/artists/{ARTIST_ID}", params={"confirm_name": "x"}
    )
    assert response.status_code == 403


# Deny by default: a member with no matching role row, an unauthenticated
# caller, and a non-member are all denied.


def test_non_member_is_denied_403(as_role):
    client = as_role("outsider-user")
    # Authenticated (login succeeded) but has no membership in the
    # workspace → 403, not 200 (BR-001 boundary, deny by default).
    assert client.get(f"/api/v1/artists/{ARTIST_ID}").status_code == 403


def test_unauthenticated_is_401(api):
    api.cookies.clear()
    assert api.get(f"/api/v1/artists/{ARTIST_ID}").status_code == 401


def test_non_member_cannot_read_workspace_via_post(as_role):
    """A non-member is 403'd on GET /workspace; POST must not become a
    back door that returns the existing singleton's data to them
    (Phase 8.3 security review, Critical). Idempotent POST when a
    workspace exists is a gated read, not an open creation path."""
    client = as_role("outsider-user")
    assert client.get("/api/v1/workspace").status_code == 403
    response = client.post("/api/v1/workspace", json={"name": "x"})
    assert response.status_code == 403, response.text


def test_member_post_workspace_is_idempotent_read(as_role):
    """A member POSTing when the workspace exists gets the existing one
    (created=False), never a second workspace."""
    client = as_role("viewer-user")
    response = client.post("/api/v1/workspace", json={"name": "ignored"})
    assert response.status_code == 200, response.text
    assert response.json()["created"] is False
