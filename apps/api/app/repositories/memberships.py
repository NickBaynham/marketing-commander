"""Workspace membership persistence (Phase 8, Increment 8.3).

Resolves a user's role within a workspace for authorization. A user with
no membership in the workspace resolves to None → denied (deny by
default, and the enforceable BR-001 cross-workspace boundary).

Traceability: REQ-054, REQ-055; BR-001; D8-4.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WorkspaceMembership


class MembershipRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def role_for(
        self, user_id: str, workspace_id: uuid.UUID
    ) -> str | None:
        result = await self._session.execute(
            select(WorkspaceMembership.role).where(
                WorkspaceMembership.user_id == user_id,
                WorkspaceMembership.workspace_id == workspace_id,
            )
        )
        return result.scalar_one_or_none()
