"""Workspace endpoints (transport wiring only).

Traceability: REQ-001; AC-024 Step 1; API-01, API-02.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import (
    get_current_user_id,
    get_membership_repository,
    get_workspace_repository,
    require,
)
from app.domain import authz
from app.api.v1.schemas import WorkspaceCreate, WorkspaceOut
from app.db import get_session
from app.repositories.memberships import MembershipRepository
from app.repositories.workspaces import WorkspaceRepository

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get(
    "",
    response_model=WorkspaceOut,
    dependencies=[Depends(require(authz.VIEW))],
)
async def get_workspace(
    workspaces: Annotated[WorkspaceRepository, Depends(get_workspace_repository)],
    _actor: Annotated[str, Depends(get_current_user_id)],
) -> WorkspaceOut:
    workspace = await workspaces.get_current()
    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "no workspace exists yet; create one first"},
        )
    return WorkspaceOut.model_validate(workspace)


@router.post("", response_model=WorkspaceOut)
async def create_workspace(
    body: WorkspaceCreate,
    workspaces: Annotated[WorkspaceRepository, Depends(get_workspace_repository)],
    memberships: Annotated[MembershipRepository, Depends(get_membership_repository)],
    actor_id: Annotated[str, Depends(get_current_user_id)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> WorkspaceOut:
    """Idempotent (REQ-001). When a workspace already exists this is
    effectively a read of the singleton, so it is authorization-gated like
    GET: a caller who is not a member is denied (403), never handed the
    workspace's data (REQ-054, BR-001). Only genuine first-run — when no
    workspace and therefore no membership can exist yet — creates without a
    role check, and the creator becomes the seeded owner."""
    existing = await workspaces.get_current()
    if existing is not None:
        role = await memberships.role_for(actor_id, existing.id)
        if role is None or not authz.is_allowed(role, authz.VIEW):
            raise HTTPException(
                status_code=403,
                detail={"message": "not a member of this workspace"},
            )
        out = WorkspaceOut.model_validate(existing)
        out.created = False
        return out
    workspace, created = await workspaces.get_or_create(body.name, actor_id)
    await session.commit()
    out = WorkspaceOut.model_validate(workspace)
    out.created = created
    return out
