"""AIP draft endpoints (transport wiring only; policy in AipService).

Error mapping: ValidationFailed -> 422 (AC-003 shape, DEC-09 total-size),
StaleVersion -> 409 (BR-019, AC-008), NotFound -> 404. Per-section size
and schema violations are rejected by AipSections at request validation
(422 via the shared handler). Save commits the draft and its audit record
together.

Traceability: REQ-006, REQ-007, REQ-012; AC-004, AC-005, AC-008;
API-09..API-11.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_aip_service
from app.api.v1.schemas import AipDraftSave, AipDraftView, AipPreviewOut
from app.db import get_session
from app.domain.aip_service import AipDraftState, AipService
from app.exceptions import NotFound, StaleVersion, ValidationFailed

router = APIRouter(prefix="/artists", tags=["aip"])

Service = Annotated[AipService, Depends(get_aip_service)]
Session = Annotated[AsyncSession, Depends(get_session)]


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
    if isinstance(exc, StaleVersion):
        raise HTTPException(status_code=409, detail={"message": str(exc)}) from exc
    if isinstance(exc, NotFound):
        raise HTTPException(status_code=404, detail={"message": str(exc)}) from exc
    raise exc


def _view(state: AipDraftState) -> AipDraftView:
    return AipDraftView(
        artist_id=state.artist_id,
        version_token=state.version_token,
        sections=state.sections,
        completeness=state.completeness,
        display_percentage=state.display_percentage,
        approval_eligible=state.approval_eligible,
        incomplete_required_sections=state.incomplete_required_sections,
    )


@router.get("/{artist_id}/aip", response_model=AipDraftView)
async def get_aip_draft(artist_id: uuid.UUID, service: Service) -> AipDraftView:
    try:
        state = await service.get_draft(artist_id)
    except Exception as exc:  # noqa: BLE001 - mapped to envelope statuses
        _raise_mapped(exc)
    return _view(state)


@router.put("/{artist_id}/aip", response_model=AipDraftView)
async def save_aip_draft(
    artist_id: uuid.UUID, body: AipDraftSave, service: Service, session: Session
) -> AipDraftView:
    try:
        state = await service.save_draft(
            artist_id,
            expected_version=body.expected_version,
            sections=body.sections,
        )
        await session.commit()
    except Exception as exc:  # noqa: BLE001
        await session.rollback()
        _raise_mapped(exc)
    return _view(state)


@router.get("/{artist_id}/aip/preview", response_model=AipPreviewOut)
async def preview_aip_draft(
    artist_id: uuid.UUID, service: Service
) -> AipPreviewOut:
    try:
        markdown = await service.preview(artist_id)
    except Exception as exc:  # noqa: BLE001
        _raise_mapped(exc)
    return AipPreviewOut(markdown=markdown)
