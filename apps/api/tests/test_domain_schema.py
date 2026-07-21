"""Domain schema invariants (Phase 5, Increment 5.1).

Runs against a scratch database migrated to head, so the assertions
exercise the real schema, constraints, and transaction semantics —
not an in-memory approximation.

Traceability: REQ-001 (idempotent workspace seed), REQ-002 (seeded
owner), REQ-003 + AC-002 (artist creation creates the empty AIP draft in
the same transaction), BR-001 (workspace_id required), D5-1
(case-insensitive per-workspace name uniqueness).
"""

import asyncio
import uuid
from collections.abc import Awaitable, Callable

import pytest
from alembic import command
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.exceptions import DuplicateArtistName
from app.models import Artist, ArtistIdentityProfile, User, Workspace
from app.repositories.artists import ArtistRepository
from app.seed import seed
from tests import factories
from tests.conftest import compose_stack_reachable
from tests.test_migrations import admin_execute, alembic_config

pytestmark = pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)


def make_scratch_db() -> tuple[str, str]:
    settings = get_settings()
    name = f"mc_domain_test_{uuid.uuid4().hex[:8]}"
    admin_execute(f'CREATE DATABASE "{name}"')
    dsn = settings.postgres_async_dsn.rsplit("/", 1)[0] + f"/{name}"
    command.upgrade(alembic_config(dsn), "head")
    return name, dsn


@pytest.fixture(scope="module")
def scratch_dsn():
    name, dsn = make_scratch_db()
    yield dsn
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


@pytest.fixture
def isolated_dsn():
    """A private scratch database for tests asserting whole-database state
    (tests own their data; no dependence on module-mates' leftovers)."""
    name, dsn = make_scratch_db()
    yield dsn
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


def run_db(dsn: str, fn: Callable[[AsyncSession], Awaitable[None]]) -> None:
    async def runner() -> None:
        engine = create_async_engine(dsn)
        try:
            async with async_sessionmaker(engine, expire_on_commit=False)() as session:
                await fn(session)
        finally:
            await engine.dispose()

    asyncio.run(runner())


def test_artist_creation_creates_empty_aip_draft_in_same_transaction(scratch_dsn):
    async def check(session: AsyncSession) -> None:
        user = await factories.create_user(session, user_id=f"u-{uuid.uuid4().hex[:6]}")
        workspace = await factories.create_workspace(session, created_by=user.id)
        artist = await factories.create_artist(session, workspace.id)
        profile = await ArtistRepository(session).get_profile(artist.id)
        assert profile is not None, "AC-002: empty AIP draft must exist with the artist"
        assert profile.workspace_id == workspace.id
        # Same-transaction semantics: rolling back discards artist AND draft.
        await session.rollback()
        assert await session.get(Artist, artist.id) is None
        result = await session.execute(
            select(ArtistIdentityProfile).where(
                ArtistIdentityProfile.artist_id == artist.id
            )
        )
        assert result.scalar_one_or_none() is None

    run_db(scratch_dsn, check)


def test_artist_name_unique_per_workspace_case_insensitive(scratch_dsn):
    async def check(session: AsyncSession) -> None:
        user = await factories.create_user(session, user_id=f"u-{uuid.uuid4().hex[:6]}")
        workspace = await factories.create_workspace(session, created_by=user.id)
        await factories.create_artist(session, workspace.id, name="CYR3NT")
        with pytest.raises(DuplicateArtistName):
            await factories.create_artist(session, workspace.id, name="cyr3nt")
        await session.rollback()

    run_db(scratch_dsn, check)


def test_artist_requires_workspace(scratch_dsn):
    async def check(session: AsyncSession) -> None:
        session.add(Artist(workspace_id=None, name="orphan"))
        with pytest.raises(IntegrityError):
            await session.flush()
        await session.rollback()

    run_db(scratch_dsn, check)


def test_artist_version_token_defaults_to_one(scratch_dsn):
    async def check(session: AsyncSession) -> None:
        user = await factories.create_user(session, user_id=f"u-{uuid.uuid4().hex[:6]}")
        workspace = await factories.create_workspace(session, created_by=user.id)
        artist = await factories.create_artist(session, workspace.id, name="Token")
        await session.commit()
        await session.refresh(artist)
        assert artist.version_token == 1
        assert artist.state == "active"

    run_db(scratch_dsn, check)


def test_workspace_singleton_enforced_by_database(isolated_dsn):
    """DEC-01/REQ-001: the unique index over a constant expression makes a
    second workspace row impossible regardless of application races."""

    async def check(session: AsyncSession) -> None:
        user = await factories.create_user(session, user_id=f"u-{uuid.uuid4().hex[:6]}")
        await factories.create_workspace(session, created_by=user.id)
        await session.commit()
        session.add(Workspace(name="Second Workspace", created_by=user.id))
        with pytest.raises(IntegrityError):
            await session.flush()
        await session.rollback()

    run_db(isolated_dsn, check)


def test_concurrent_update_raises_stale_version(isolated_dsn):
    """BR-019 under real concurrency: the versioned UPDATE conditions on
    the loaded version, so a second writer holding a stale row loses."""

    async def check(_session: AsyncSession) -> None:
        from sqlalchemy.pool import NullPool

        from app.exceptions import StaleVersion
        from app.repositories.artists import ArtistRepository

        engine_a = create_async_engine(isolated_dsn, poolclass=NullPool)
        engine_b = create_async_engine(isolated_dsn, poolclass=NullPool)
        try:
            maker_a = async_sessionmaker(engine_a, expire_on_commit=False)
            maker_b = async_sessionmaker(engine_b, expire_on_commit=False)
            async with maker_a() as setup:
                user = await factories.create_user(
                    setup, user_id=f"u-{uuid.uuid4().hex[:6]}"
                )
                workspace = await factories.create_workspace(
                    setup, created_by=user.id
                )
                artist = await factories.create_artist(
                    setup, workspace.id, name="Raced"
                )
                await setup.commit()
                artist_id = artist.id
            async with maker_a() as sa, maker_b() as sb:
                loaded_a = await sa.get(Artist, artist_id)
                loaded_b = await sb.get(Artist, artist_id)
                loaded_a.summary = "writer A"
                await ArtistRepository(sa).save(loaded_a)
                await sa.commit()
                loaded_b.summary = "writer B"
                with pytest.raises(StaleVersion):
                    await ArtistRepository(sb).save(loaded_b)
                await sb.rollback()
        finally:
            await engine_a.dispose()
            await engine_b.dispose()

    run_db(isolated_dsn, check)


def test_seed_is_idempotent(isolated_dsn):
    async def check(session: AsyncSession) -> None:
        first = await seed(session)
        await session.commit()
        second = await seed(session)
        await session.commit()
        assert first == {
            "user": "created",
            "workspace": "created",
            "membership": "created",
        }
        assert second == {
            "user": "exists",
            "workspace": "exists",
            "membership": "exists",
        }
        assert (await session.execute(select(func.count(Workspace.id)))).scalar() == 1
        assert (await session.execute(select(func.count(User.id)))).scalar() == 1

    run_db(isolated_dsn, check)
