"""Audit persistence: append-only records with non-null actor (BR-020).

Traceability: REQ-040; Phase 5 Increment 5.2.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditRecord


class AuditRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record(
        self,
        actor_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        correlation_id: str | None = None,
    ) -> None:
        self._session.add(
            AuditRecord(
                actor_id=actor_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                correlation_id=correlation_id,
            )
        )
        await self._session.flush()
