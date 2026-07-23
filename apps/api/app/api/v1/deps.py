"""v1 dependency wiring (transport layer).

Phase 8: identity now comes from a validated server-side session
(`get_current_user_id`), replacing the pre-auth permissive hook. The
authenticated id is the same seeded `local-owner` domain id, so approval
and audit provenance is unchanged (DEC-03). Authorization by role is
enforced in Increment 8.3; here every product route requires a valid
session (401 otherwise).

Traceability: REQ-052, REQ-053, REQ-055; DEC-03; D8-2, D8-5.
"""

import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_session
from app.domain.aip_approval import AipApprovalService
from app.domain.aip_service import AipService
from app.domain.artists import ArtistService
from app.domain.auth import AuthService
from app.redis_client import get_loop_redis
from app.repositories.aip import AipRepository
from app.repositories.aip_versions import AipVersionRepository
from app.repositories.artists import ArtistRepository
from app.repositories.audit import AuditRepository
from app.repositories.users import UserRepository
from app.repositories.workspaces import WorkspaceRepository
from app.sessions import SessionStore


def session_cookie_name() -> str:
    return get_settings().session_cookie_name


def read_session_cookie(request: Request) -> str | None:
    return request.cookies.get(session_cookie_name())


def set_session_cookie(response: Response, token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_absolute_ttl_seconds,
        httponly=True,
        samesite="lax",
        secure=settings.session_cookie_secure,
        path="/",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=session_cookie_name(), httponly=True, samesite="lax", path="/"
    )


def get_session_store() -> SessionStore:
    settings = get_settings()
    return SessionStore(
        get_loop_redis,
        idle_ttl=settings.session_idle_ttl_seconds,
        absolute_ttl=settings.session_absolute_ttl_seconds,
    )


def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthService:
    return AuthService(users=UserRepository(session), sessions=get_session_store())


async def get_current_user_id(request: Request) -> str:
    """Authenticated identity from the session cookie, or 401. This is
    the single authentication gate for product routes (DEC-03)."""
    user_id = await get_session_store().resolve(read_session_cookie(request))
    if user_id is None:
        raise HTTPException(
            status_code=401, detail={"message": "authentication required"}
        )
    return user_id


def get_workspace_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> WorkspaceRepository:
    return WorkspaceRepository(session)


def get_artist_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    actor_id: Annotated[str, Depends(get_current_user_id)],
) -> ArtistService:
    return ArtistService(
        artists=ArtistRepository(session),
        audit=AuditRepository(session),
        actor_id=actor_id,
    )


def get_aip_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    actor_id: Annotated[str, Depends(get_current_user_id)],
) -> AipService:
    return AipService(
        aip=AipRepository(session),
        audit=AuditRepository(session),
        actor_id=actor_id,
    )


def get_aip_approval_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    actor_id: Annotated[str, Depends(get_current_user_id)],
) -> AipApprovalService:
    return AipApprovalService(
        aip=AipRepository(session),
        versions=AipVersionRepository(session),
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
