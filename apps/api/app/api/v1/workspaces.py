"""Workspace endpoints (transport wiring only).

Traceability: REQ-001; AC-024 Step 1; API-01, API-02.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_actor_id, get_workspace_repository
from app.api.v1.schemas import WorkspaceCreate, WorkspaceOut
from app.db import get_session
from app.repositories.workspaces import WorkspaceRepository

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("", response_model=WorkspaceOut)
async def get_workspace(
    workspaces: Annotated[WorkspaceRepository, Depends(get_workspace_repository)],
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
    actor_id: Annotated[str, Depends(get_actor_id)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> WorkspaceOut:
    workspace, created = await workspaces.get_or_create(body.name, actor_id)
    await session.commit()
    out = WorkspaceOut.model_validate(workspace)
    out.created = created
    return out
