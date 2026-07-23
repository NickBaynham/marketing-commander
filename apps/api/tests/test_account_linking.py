"""AC-030 — account linking preserves history (Phase 8, DEC-03).

Proves the strong claim the 8.2 review flagged as unverified: a provenance
record created BEFORE authentication existed is byte-identical after the
credential migration (687c205cf24f) is applied and the owner is linked
(password set in place). Two angles:

- the real migration transition on a standalone audit_records row (the
  table has no FK chain, so it is inserted at the pre-credential revision
  and compared across the upgrade + link);
- an approvals row (full aggregate) created pre-link and compared after
  the in-place credential update.

Traceability: AC-030, REQ-056; DEC-03, ADR-002; BR-020; D8-5.
"""

import asyncio
import uuid

import asyncpg
import pytest
from alembic import command
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.models import Approval, Artist, ArtistIdentityProfile, User, Workspace
from app.repositories.aip_versions import AipVersionRepository
from app.security import hash_password
from tests.conftest import compose_stack_reachable
from tests.test_migrations import admin_execute, alembic_config

PRE_CREDENTIAL_REVISION = "3522ec8dfd5d"  # down_revision of 687c205cf24f
OWNER_ID = "local-owner"

pytestmark = pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)


def _run(coro):
    return asyncio.run(coro)


async def _fetchrow(dsn: str, sql: str, *args) -> dict:
    conn = await asyncpg.connect(dsn)
    try:
        row = await conn.fetchrow(sql, *args)
        return dict(row) if row else {}
    finally:
        await conn.close()


async def _execute(dsn: str, sql: str, *args) -> None:
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(sql, *args)
    finally:
        await conn.close()


@pytest.fixture
def scratch():
    settings = get_settings()
    name = f"mc_link_test_{uuid.uuid4().hex[:8]}"
    admin_execute(f'CREATE DATABASE "{name}"')
    sync = settings.postgres_dsn.rsplit("/", 1)[0] + f"/{name}"
    asyncpg_dsn = sync  # asyncpg speaks the plain postgres URL
    async_dsn = settings.postgres_async_dsn.rsplit("/", 1)[0] + f"/{name}"
    yield {"name": name, "asyncpg": asyncpg_dsn, "async": async_dsn}
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


def test_credential_migration_leaves_pre_existing_audit_record_byte_identical(scratch):
    """The real AC-030 sequence for an audit row: written before the
    credential column existed, unchanged after the migration and link."""
    # Migrate to the revision BEFORE credentials existed.
    command.upgrade(alembic_config(scratch["async"]), PRE_CREDENTIAL_REVISION)

    audit_id = uuid.uuid4()

    async def seed_history() -> None:
        # users has no password_hash column at this revision.
        await _execute(
            scratch["asyncpg"],
            "INSERT INTO users (id, display_name, identity_source, created_at, "
            "updated_at) VALUES ($1, 'Nick', 'local_seed', now(), now())",
            OWNER_ID,
        )
        await _execute(
            scratch["asyncpg"],
            "INSERT INTO audit_records (id, actor_id, action, entity_type, "
            "entity_id, correlation_id, created_at) "
            "VALUES ($1, $2, 'aip.approved', 'aip_version', $3, 'corr-1', now())",
            audit_id,
            OWNER_ID,
            str(uuid.uuid4()),
        )

    _run(seed_history())

    before = _run(
        _fetchrow(
            scratch["asyncpg"],
            "SELECT * FROM audit_records WHERE id = $1",
            audit_id,
        )
    )
    assert before["actor_id"] == OWNER_ID

    # Apply the credential migration and link the owner in place.
    command.upgrade(alembic_config(scratch["async"]), "head")
    _run(
        _execute(
            scratch["asyncpg"],
            "UPDATE users SET password_hash = $1 WHERE id = $2",
            hash_password("dev-password"),
            OWNER_ID,
        )
    )

    after = _run(
        _fetchrow(
            scratch["asyncpg"],
            "SELECT * FROM audit_records WHERE id = $1",
            audit_id,
        )
    )
    # Byte-identical: every field, including actor id and timestamp.
    assert after == before
    # The owner is the same domain id, now carrying a credential.
    owner = _run(
        _fetchrow(
            scratch["asyncpg"],
            "SELECT id, password_hash FROM users WHERE id = $1",
            OWNER_ID,
        )
    )
    assert owner["id"] == OWNER_ID
    assert owner["password_hash"] is not None


def test_linking_credential_preserves_the_approval_record(scratch):
    """An approval created by the owner while no password existed is
    unchanged after the credential is set in place (the linking step)."""
    command.upgrade(alembic_config(scratch["async"]), "head")
    engine = create_async_engine(scratch["async"], poolclass=NullPool)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def build_and_check() -> None:
        try:
            async with maker() as s:
                # Owner exists WITHOUT a password — the pre-auth state.
                owner = User(
                    id=OWNER_ID, display_name="Nick", identity_source="local_seed"
                )
                s.add(owner)
                ws = Workspace(name="CYR3NT Workspace", created_by=OWNER_ID)
                s.add(ws)
                await s.flush()
                artist = Artist(workspace_id=ws.id, name="CYR3NT")
                s.add(artist)
                await s.flush()
                aip = ArtistIdentityProfile(
                    artist_id=artist.id, workspace_id=ws.id, sections={}
                )
                s.add(aip)
                await s.flush()
                repo = AipVersionRepository(s)
                version = await repo.create_version(
                    aip_id=aip.id,
                    workspace_id=ws.id,
                    version_number=1,
                    sections={},
                    created_from_token=1,
                    created_by=OWNER_ID,
                )
                await repo.create_approval(version_id=version.id, actor_id=OWNER_ID)
                await s.commit()
                approval_before = (
                    await s.execute(select(Approval).where(Approval.version_id == version.id))
                ).scalar_one()
                snapshot = {
                    "id": approval_before.id,
                    "version_id": approval_before.version_id,
                    "actor_id": approval_before.actor_id,
                    "created_at": approval_before.created_at,
                }

            # Link the owner: set the password in place (what seed does).
            async with maker() as s:
                owner = await s.get(User, OWNER_ID)
                owner.password_hash = hash_password("dev-password")
                await s.commit()

            # The approval row is byte-identical; the actor is still the
            # same domain id (AC-030, BR-020).
            async with maker() as s:
                approval_after = (
                    await s.execute(select(Approval).where(Approval.id == snapshot["id"]))
                ).scalar_one()
                assert approval_after.version_id == snapshot["version_id"]
                assert approval_after.actor_id == snapshot["actor_id"] == OWNER_ID
                assert approval_after.created_at == snapshot["created_at"]
                linked = await s.get(User, OWNER_ID)
                assert linked.id == OWNER_ID
                assert linked.password_hash is not None
        finally:
            await engine.dispose()

    _run(build_and_check())
