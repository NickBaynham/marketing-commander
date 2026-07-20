"""Artist endpoints (transport wiring only; policy in ArtistService).

Error mapping: ValidationFailed -> 422 (AC-003 shape), StaleVersion ->
409 (BR-019), ArtistArchived -> 409 (BR-014), NotFound -> 404,
unconfirmed deletion -> 422 (BR-015). Every state change commits the
service work and its audit record together.

Traceability: REQ-003, REQ-004, REQ-005, REQ-051; AC-002, AC-003,
AC-025; API-03..API-08.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_artist_service, get_current_workspace_id
from app.api.v1.schemas import (
    ArtistCreate,
    ArtistOut,
    ArtistUpdate,
    DeletionOut,
    VersionedAction,
)
from app.db import get_session
from app.domain.artists import ArtistService
from app.exceptions import (
    ArtistArchived,
    DuplicateArtistName,
    NotFound,
    StaleVersion,
    ValidationFailed,
)

router = APIRouter(prefix="/artists", tags=["artists"])

Service = Annotated[ArtistService, Depends(get_artist_service)]
Session = Annotated[AsyncSession, Depends(get_session)]
WorkspaceId = Annotated[uuid.UUID, Depends(get_current_workspace_id)]


def _raise_mapped(exc: Exception) -> None:
    if isinstance(exc, ValidationFailed):
        raise HTTPException(
            status_code=422,
            detail={
                "message": exc.message,
                "details": [
                    {"field": exc.field, "rule": exc.rule, "message": exc.message}
                ],
            },
        ) from exc
    if isinstance(exc, DuplicateArtistName):
        raise HTTPException(
            status_code=422,
            detail={
                "message": "artist name already exists in this workspace",
                "details": [
                    {
                        "field": "name",
                        "rule": "unique_per_workspace",
                        "message": "artist name already exists in this workspace",
                    }
                ],
            },
        ) from exc
    if isinstance(exc, StaleVersion):
        raise HTTPException(
            status_code=409, detail={"message": str(exc)}
        ) from exc
    if isinstance(exc, ArtistArchived):
        raise HTTPException(
            status_code=409, detail={"message": str(exc)}
        ) from exc
    if isinstance(exc, NotFound):
        raise HTTPException(
            status_code=404, detail={"message": str(exc)}
        ) from exc
    raise exc


@router.post("", response_model=ArtistOut, status_code=201)
async def create_artist(
    body: ArtistCreate, service: Service, session: Session, workspace_id: WorkspaceId
) -> ArtistOut:
    try:
        artist = await service.create(
            workspace_id=workspace_id,
            name=body.name,
            genre=body.genre,
            summary=body.summary,
        )
        await session.commit()
    except Exception as exc:  # noqa: BLE001 - mapped to envelope statuses
        await session.rollback()
        _raise_mapped(exc)
    return ArtistOut.model_validate(artist)


@router.get("", response_model=list[ArtistOut])
async def list_artists(
    service: Service, workspace_id: WorkspaceId
) -> list[ArtistOut]:
    artists = await service.list_for_workspace(workspace_id)
    return [ArtistOut.model_validate(a) for a in artists]


@router.get("/{artist_id}", response_model=ArtistOut)
async def get_artist(artist_id: uuid.UUID, service: Service) -> ArtistOut:
    try:
        artist = await service.get(artist_id)
    except Exception as exc:  # noqa: BLE001
        _raise_mapped(exc)
    return ArtistOut.model_validate(artist)


@router.patch("/{artist_id}", response_model=ArtistOut)
async def update_artist(
    artist_id: uuid.UUID, body: ArtistUpdate, service: Service, session: Session
) -> ArtistOut:
    try:
        artist = await service.update(
            artist_id,
            expected_version=body.expected_version,
            name=body.name,
            genre=body.genre,
            summary=body.summary,
        )
        await session.commit()
    except Exception as exc:  # noqa: BLE001
        await session.rollback()
        _raise_mapped(exc)
    return ArtistOut.model_validate(artist)


@router.post("/{artist_id}/archive", response_model=ArtistOut)
async def archive_artist(
    artist_id: uuid.UUID, body: VersionedAction, service: Service, session: Session
) -> ArtistOut:
    try:
        artist = await service.archive(artist_id, body.expected_version)
        await session.commit()
    except Exception as exc:  # noqa: BLE001
        await session.rollback()
        _raise_mapped(exc)
    return ArtistOut.model_validate(artist)


@router.post("/{artist_id}/restore", response_model=ArtistOut)
async def restore_artist(
    artist_id: uuid.UUID, body: VersionedAction, service: Service, session: Session
) -> ArtistOut:
    try:
        artist = await service.restore(artist_id, body.expected_version)
        await session.commit()
    except Exception as exc:  # noqa: BLE001
        await session.rollback()
        _raise_mapped(exc)
    return ArtistOut.model_validate(artist)


@router.delete("/{artist_id}", response_model=DeletionOut)
async def delete_artist(
    artist_id: uuid.UUID,
    service: Service,
    session: Session,
    confirm: bool = False,
) -> DeletionOut:
    try:
        removed = await service.delete(artist_id, confirmed=confirm)
        await session.commit()
    except Exception as exc:  # noqa: BLE001
        await session.rollback()
        _raise_mapped(exc)
    return DeletionOut(removed=removed)
