"""v1 dependency wiring (transport layer).

Known limitation (Phase 8): the seeded local owner is the only actor and
no real access control exists; this dependency is the single enforcement
point that Phase 8 replaces with authenticated identity and the
role-action matrix.

Traceability: DEC-03; Phase 5 authorization note.
"""

import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.domain.aip_service import AipService
from app.domain.artists import ArtistService
from app.repositories.aip import AipRepository
from app.repositories.artists import ArtistRepository
from app.repositories.audit import AuditRepository
from app.repositories.workspaces import WorkspaceRepository

LOCAL_OWNER_ID = "local-owner"


def get_actor_id() -> str:
    return LOCAL_OWNER_ID


def get_workspace_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> WorkspaceRepository:
    return WorkspaceRepository(session)


def get_artist_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    actor_id: Annotated[str, Depends(get_actor_id)],
) -> ArtistService:
    return ArtistService(
        artists=ArtistRepository(session),
        audit=AuditRepository(session),
        actor_id=actor_id,
    )


def get_aip_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    actor_id: Annotated[str, Depends(get_actor_id)],
) -> AipService:
    return AipService(
        aip=AipRepository(session),
        audit=AuditRepository(session),
        actor_id=actor_id,
    )


async def get_current_workspace_id(
    workspaces: Annotated[WorkspaceRepository, Depends(get_workspace_repository)],
) -> uuid.UUID:
    workspace = await workspaces.get_current()
    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "no workspace exists yet; create one first"},
        )
    return workspace.id
