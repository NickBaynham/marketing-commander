"""AIP version endpoints (transport wiring only).

Read-only: an immutable version is fetched by id (API-14) or rendered as
Markdown for export (D7-6). No update or delete route exists on
versions — the API half of the two-layer immutability guarantee
(REQ-014); the DB trigger is the other half.

Traceability: REQ-014; AC-005, AC-007; API-14; D7-6.
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.aip import _version_out
from app.api.v1.deps import get_aip_approval_service
from app.api.v1.schemas import AipVersionExportOut, AipVersionOut
from app.domain.aip_approval import AipApprovalService
from app.exceptions import NotFound

router = APIRouter(prefix="/aip-versions", tags=["aip-versions"])

Approvals = Annotated[AipApprovalService, Depends(get_aip_approval_service)]


def _raise_mapped(exc: Exception) -> None:
    if isinstance(exc, NotFound):
        raise HTTPException(status_code=404, detail={"message": str(exc)}) from exc
    raise exc


@router.get("/{version_id}", response_model=AipVersionOut)
async def get_aip_version(
    version_id: uuid.UUID, approvals: Approvals
) -> AipVersionOut:
    try:
        view = await approvals.get_version(version_id)
    except Exception as exc:  # noqa: BLE001 - mapped to envelope statuses
        _raise_mapped(exc)
    return _version_out(view)


@router.get("/{version_id}/export", response_model=AipVersionExportOut)
async def export_aip_version(
    version_id: uuid.UUID, approvals: Approvals
) -> AipVersionExportOut:
    try:
        markdown = await approvals.export_markdown(version_id)
    except Exception as exc:  # noqa: BLE001
        _raise_mapped(exc)
    return AipVersionExportOut(markdown=markdown)
