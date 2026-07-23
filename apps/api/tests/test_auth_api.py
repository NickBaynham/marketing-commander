"""Authentication API tests (Phase 8, Increment 8.2).

Full-stack against a scratch database and the real Redis session store,
with the identity gate NOT overridden — this is the suite that exercises
the real login → session → 401 path and the DEC-03 linking guarantee.

Traceability: REQ-052, REQ-053, REQ-054; AC-026, AC-027, AC-028; DEC-03;
D8-2, D8-3, D8-5; ASVS V2, V3.
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

OWNER_ID = "local-owner"
OWNER_PW = "correct-horse-owner-pw"

# Set by the api fixture so the DEC-03 test can read the same scratch DB
# the client writes to (the fixture owns the only other handle).
_SCRATCH_DSN: str | None = None


@pytest.fixture(scope="module")
def api():
    global _SCRATCH_DSN
    from app.db import get_session
    from app.identity import IDENTITY_SOURCE, LOCAL_OWNER_DISPLAY_NAME
    from app.main import create_app
    from app.models import User
    from app.security import hash_password

    name, dsn = make_scratch_db()
    _SCRATCH_DSN = dsn
    engine = create_async_engine(dsn, poolclass=NullPool)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def seed_owner():
        async with maker() as session:
            session.add(
                User(
                    id=OWNER_ID,
                    display_name=LOCAL_OWNER_DISPLAY_NAME,
                    identity_source=IDENTITY_SOURCE,
                    password_hash=hash_password(OWNER_PW),
                )
            )
            await session.commit()

    asyncio.run(seed_owner())

    async def override_session():
        async with maker() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    # Note: get_current_user_id is intentionally NOT overridden here.
    client = TestClient(app)
    yield client
    client.close()
    asyncio.run(engine.dispose())
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


@pytest.fixture
def fresh_client(api):
    api.cookies.clear()
    return api


def login(client: TestClient, username=OWNER_ID, password=OWNER_PW):
    return client.post(
        "/api/v1/auth/login", json={"username": username, "password": password}
    )


# Login (AC-026)


def test_login_success_sets_session_cookie(fresh_client):
    response = login(fresh_client)
    assert response.status_code == 200
    assert response.json() == {"user_id": OWNER_ID}
    cookie = response.headers.get("set-cookie", "").lower()
    assert "mc_session=" in cookie
    assert "httponly" in cookie  # not readable from JavaScript
    assert "samesite=lax" in cookie  # CSRF mitigation (Starlette lowercases)


def test_login_wrong_password_401(fresh_client):
    response = login(fresh_client, password="nope")
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "invalid username or password"


def test_login_unknown_user_401_same_message(fresh_client):
    # No enumeration: unknown user and wrong password read identically.
    response = login(fresh_client, username="ghost")
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "invalid username or password"


# Session gate (AC-028)


def test_protected_route_requires_session(fresh_client):
    response = fresh_client.get("/api/v1/workspace")
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "authentication required"


def test_session_grants_access_then_logout_revokes(fresh_client):
    login(fresh_client)
    # /me reflects the authenticated identity.
    me = fresh_client.get("/api/v1/auth/me")
    assert me.status_code == 200 and me.json() == {"user_id": OWNER_ID}
    # A protected route is reachable (404 = authenticated but no workspace
    # yet; crucially not 401).
    assert fresh_client.get("/api/v1/workspace").status_code == 404
    # Logout revokes the session immediately.
    assert fresh_client.post("/api/v1/auth/logout").status_code == 204
    assert fresh_client.get("/api/v1/auth/me").status_code == 401


def test_tampered_cookie_is_rejected(fresh_client):
    login(fresh_client)
    fresh_client.cookies.set("mc_session", "not-a-real-token")
    assert fresh_client.get("/api/v1/auth/me").status_code == 401


# DEC-03 linking (AC-027): the authenticated owner IS local-owner; a
# protected write records that exact actor, no new user is created.


def test_authenticated_actions_use_the_seeded_owner_id(fresh_client):
    login(fresh_client)
    fresh_client.post("/api/v1/workspace", json={"name": "CYR3NT Workspace"})
    artist = fresh_client.post(
        "/api/v1/artists", json={"name": f"E2E {uuid.uuid4().hex[:6]}"}
    )
    assert artist.status_code == 201
    # The audit actor for the create is the seeded owner id, proving the
    # session identity linked to the existing domain user (DEC-03) rather
    # than minting a new actor. Read the same scratch DB the client wrote.
    assert _SCRATCH_DSN is not None
    engine = create_async_engine(_SCRATCH_DSN, poolclass=NullPool)
    try:
        actor, user_count = asyncio.run(_owner_audit_and_user_count(engine))
    finally:
        asyncio.run(engine.dispose())
    assert actor == OWNER_ID
    # Linking added no new user; the seeded owner is still the only one.
    assert user_count == 1


async def _owner_audit_and_user_count(engine):
    from sqlalchemy import text

    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as session:
        actor = (
            await session.execute(
                text(
                    "SELECT actor_id FROM audit_records "
                    "WHERE entity_type='artist' ORDER BY created_at DESC LIMIT 1"
                )
            )
        ).scalar()
        users = (
            await session.execute(text("SELECT count(*) FROM users"))
        ).scalar()
        return actor, users
