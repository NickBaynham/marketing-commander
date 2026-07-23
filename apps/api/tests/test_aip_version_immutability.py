"""Persistence-level immutability of approved versions (Phase 7, 7.1).

Proves the DB half of the two-layer guarantee (REQ-014, ADR-005, D7-3)
against the application role: UPDATE of a version or approval row raises,
while DELETE via the BR-015 artist-aggregate cascade still succeeds
(the trigger blocks UPDATE only, by design). The domain half — no update
path — is enforced by the insert-only repository and the layering test.

Traceability: REQ-014, REQ-015; BR-005, BR-006, BR-015; ADR-005; D7-3.
"""

import asyncio
import uuid

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models import (
    Approval,
    Artist,
    ArtistIdentityProfile,
    ArtistIdentityProfileVersion,
    User,
    Workspace,
)
from app.repositories.aip_versions import AipVersionRepository
from tests.conftest import compose_stack_reachable
from tests.test_domain_schema import make_scratch_db
from tests.test_migrations import admin_execute

pytestmark = pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)


@pytest.fixture(scope="module")
def scratch():
    name, dsn = make_scratch_db()
    yield dsn
    admin_execute(f'DROP DATABASE "{name}" WITH (FORCE)')


async def _make_version(dsn: str, artist_name: str, numbers: list[int]) -> dict:
    """Create an artist, profile, and one version per number, returning ids."""
    engine = create_async_engine(dsn, poolclass=NullPool)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with maker() as s:
            if await s.get(User, "local-owner") is None:
                s.add(
                    User(
                        id="local-owner",
                        display_name="Nick",
                        identity_source="local_seed",
                    )
                )
                await s.flush()
            # One workspace per database (the B2 singleton constraint);
            # every artist in this scratch DB shares it.
            ws = (
                await s.execute(select(Workspace).limit(1))
            ).scalar_one_or_none()
            if ws is None:
                ws = Workspace(name="CYR3NT Workspace", created_by="local-owner")
                s.add(ws)
                await s.flush()
            artist = Artist(workspace_id=ws.id, name=artist_name)
            s.add(artist)
            await s.flush()
            profile = ArtistIdentityProfile(
                artist_id=artist.id, workspace_id=ws.id, sections={}
            )
            s.add(profile)
            await s.flush()
            repo = AipVersionRepository(s)
            versions = []
            for n in numbers:
                v = await repo.create_version(
                    aip_id=profile.id,
                    workspace_id=ws.id,
                    version_number=n,
                    sections={"core_identity": {"content": f"snapshot {n}"}},
                    created_from_token=n,
                    created_by="local-owner",
                )
                versions.append(v.id)
            approval = await repo.create_approval(
                version_id=versions[-1], actor_id="local-owner"
            )
            await s.commit()
            return {
                "artist": artist.id,
                "aip": profile.id,
                "versions": versions,
                "approval": approval.id,
            }
    finally:
        await engine.dispose()


def _run(coro):
    return asyncio.run(coro)


def test_version_update_is_blocked_for_the_app_role(scratch):
    ids = _run(_make_version(scratch, "Immutable One", [1]))

    async def attempt():
        engine = create_async_engine(scratch, poolclass=NullPool)
        try:
            async with async_sessionmaker(engine)() as s:
                with pytest.raises(DBAPIError, match="immutable row"):
                    await s.execute(
                        text(
                            "UPDATE artist_identity_profile_versions "
                            "SET version_number = 99 WHERE id = :id"
                        ),
                        {"id": ids["versions"][0]},
                    )
        finally:
            await engine.dispose()

    _run(attempt())


def test_approval_update_is_blocked_for_the_app_role(scratch):
    ids = _run(_make_version(scratch, "Immutable Two", [1]))

    async def attempt():
        engine = create_async_engine(scratch, poolclass=NullPool)
        try:
            async with async_sessionmaker(engine)() as s:
                with pytest.raises(DBAPIError, match="immutable row"):
                    await s.execute(
                        text("UPDATE approvals SET note = 'tampered' WHERE id = :id"),
                        {"id": ids["approval"]},
                    )
        finally:
            await engine.dispose()

    _run(attempt())


def test_aggregate_deletion_cascades_through_the_trigger(scratch):
    """BR-015: deleting the artist removes its versions and approvals via
    cascade — the UPDATE-only trigger does not block DELETE."""
    ids = _run(_make_version(scratch, "Deletable Artist", [1, 2]))

    async def delete_and_count():
        engine = create_async_engine(scratch, poolclass=NullPool)
        try:
            async with async_sessionmaker(engine)() as s:
                artist = await s.get(Artist, ids["artist"])
                await s.execute(
                    text(
                        "DELETE FROM artist_identity_profiles WHERE artist_id = :a"
                    ),
                    {"a": ids["artist"]},
                )
                await s.delete(artist)
                await s.commit()
                remaining = await s.execute(
                    select(func.count())
                    .select_from(ArtistIdentityProfileVersion)
                    .where(ArtistIdentityProfileVersion.aip_id == ids["aip"])
                )
                approvals = await s.execute(
                    select(func.count())
                    .select_from(Approval)
                    .where(Approval.id == ids["approval"])
                )
                return remaining.scalar_one(), approvals.scalar_one()
        finally:
            await engine.dispose()

    version_count, approval_count = _run(delete_and_count())
    assert version_count == 0
    assert approval_count == 0


def test_superseding_inserts_and_leaves_prior_version_byte_identical(scratch):
    """REQ-015: a second version supersedes by insert; version 1's stored
    snapshot is unchanged."""
    ids = _run(_make_version(scratch, "Supersede Artist", [1]))

    async def check():
        engine = create_async_engine(scratch, poolclass=NullPool)
        try:
            async with async_sessionmaker(engine)() as s:
                v1_before = (
                    await s.get(ArtistIdentityProfileVersion, ids["versions"][0])
                ).sections
                repo = AipVersionRepository(s)
                numbers = await repo.existing_numbers(ids["aip"])
                assert numbers == [1]
                await repo.create_version(
                    aip_id=ids["aip"],
                    workspace_id=(
                        await s.get(
                            ArtistIdentityProfileVersion, ids["versions"][0]
                        )
                    ).workspace_id,
                    version_number=2,
                    sections={"core_identity": {"content": "snapshot 2 revised"}},
                    created_from_token=2,
                    created_by="local-owner",
                )
                await s.commit()
                v1_after = (
                    await s.get(ArtistIdentityProfileVersion, ids["versions"][0])
                ).sections
                return v1_before, v1_after

        finally:
            await engine.dispose()

    before, after = _run(check())
    assert before == after == {"core_identity": {"content": "snapshot 1"}}
