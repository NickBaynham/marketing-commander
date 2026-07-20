"""Workspace persistence (Phase 5, Increment 5.2).

The MVP holds exactly one workspace (DEC-01); creation is idempotent —
a second attempt returns the existing workspace (REQ-001, golden path
Step 1).

Traceability: REQ-001; BR-001; DEC-01.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Workspace, WorkspaceMembership


class WorkspaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_current(self) -> Workspace | None:
        result = await self._session.execute(
            select(Workspace).order_by(Workspace.created_at)
        )
        return result.scalars().first()

    async def get_or_create(self, name: str, actor_id: str) -> tuple[Workspace, bool]:
        existing = await self.get_current()
        if existing is not None:
            return existing, False
        if await self._session.get(User, actor_id) is None:
            self._session.add(
                User(id=actor_id, display_name=actor_id, identity_source="local_seed")
            )
            await self._session.flush()
        workspace = Workspace(name=name, created_by=actor_id)
        self._session.add(workspace)
        await self._session.flush()
        self._session.add(
            WorkspaceMembership(
                user_id=actor_id,
                workspace_id=workspace.id,
                role="owner",
                granted_by=actor_id,
            )
        )
        await self._session.flush()
        return workspace, True
