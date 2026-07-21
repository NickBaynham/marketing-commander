"""Workspace persistence (Phase 5, Increment 5.2; hardened post-review).

The MVP holds exactly one workspace (DEC-01), enforced at the database
level by a singleton unique index — concurrent first-run creations
collapse to one row, with the loser returning the winner's workspace
(REQ-001). Creation writes audit records for every record it
materializes (BR-020, REQ-040).

Traceability: REQ-001, REQ-040; BR-001, BR-020; DEC-01, DEC-03.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.correlation import get_correlation_id
from app.identity import IDENTITY_SOURCE, LOCAL_OWNER_DISPLAY_NAME
from app.models import User, Workspace, WorkspaceMembership
from app.repositories.audit import AuditRepository


class WorkspaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._audit = AuditRepository(session)

    async def get_current(self) -> Workspace | None:
        result = await self._session.execute(
            select(Workspace).order_by(Workspace.created_at)
        )
        return result.scalars().first()

    async def _record(self, actor_id: str, action: str, entity: str, entity_id):
        await self._audit.record(
            actor_id=actor_id,
            action=action,
            entity_type=entity,
            entity_id=str(entity_id),
            correlation_id=get_correlation_id(),
        )

    async def get_or_create(self, name: str, actor_id: str) -> tuple[Workspace, bool]:
        existing = await self.get_current()
        if existing is not None:
            return existing, False
        try:
            async with self._session.begin_nested():
                if await self._session.get(User, actor_id) is None:
                    self._session.add(
                        User(
                            id=actor_id,
                            display_name=LOCAL_OWNER_DISPLAY_NAME,
                            identity_source=IDENTITY_SOURCE,
                        )
                    )
                    await self._session.flush()
                    await self._record(actor_id, "user.created", "user", actor_id)
                workspace = Workspace(name=name, created_by=actor_id)
                self._session.add(workspace)
                await self._session.flush()
                membership = WorkspaceMembership(
                    user_id=actor_id,
                    workspace_id=workspace.id,
                    role="owner",
                    granted_by=actor_id,
                )
                self._session.add(membership)
                await self._session.flush()
                await self._record(
                    actor_id, "workspace.created", "workspace", workspace.id
                )
                await self._record(
                    actor_id, "membership.created", "membership", membership.id
                )
        except IntegrityError:
            # The singleton index fired: a concurrent creator won the
            # race. The savepoint rolled our insert back; return theirs.
            existing = await self.get_current()
            if existing is None:
                raise
            return existing, False
        return workspace, True
