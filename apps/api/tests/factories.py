"""Entity factories (Test Data Strategy, Phase 5 Increment 5.1).

Async factory helpers with deterministic CYR3NT defaults matching
tests/fixtures/cyr3nt/seed.json. Each factory persists through the same
repository/session machinery production uses; tests own their data and
never depend on another test's leftovers.

Traceability: Test Data Strategy (plan Cross-Cutting Requirements);
DEC-01, DEC-03.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Artist, User, Workspace, WorkspaceMembership
from app.repositories.artists import ArtistRepository

CYR3NT_NAME = "CYR3NT"
CYR3NT_GENRE = "melodic techno"


async def create_user(
    session: AsyncSession,
    user_id: str = "local-owner",
    display_name: str = "Nick",
) -> User:
    user = User(id=user_id, display_name=display_name, identity_source="local_seed")
    session.add(user)
    await session.flush()
    return user


async def create_workspace(
    session: AsyncSession,
    created_by: str,
    name: str = "CYR3NT Workspace",
) -> Workspace:
    workspace = Workspace(name=name, created_by=created_by)
    session.add(workspace)
    await session.flush()
    return workspace


async def create_membership(
    session: AsyncSession,
    user_id: str,
    workspace_id: uuid.UUID,
    role: str = "owner",
) -> WorkspaceMembership:
    membership = WorkspaceMembership(
        user_id=user_id, workspace_id=workspace_id, role=role, granted_by=user_id
    )
    session.add(membership)
    await session.flush()
    return membership


async def create_artist(
    session: AsyncSession,
    workspace_id: uuid.UUID,
    name: str = CYR3NT_NAME,
    genre: str | None = CYR3NT_GENRE,
) -> Artist:
    return await ArtistRepository(session).create(
        workspace_id=workspace_id, name=name, genre=genre
    )
