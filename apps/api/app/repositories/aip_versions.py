"""AIP version and approval persistence (Phase 7, Increment 7.1).

Insert-only: this repository creates and reads immutable version and
approval rows; it exposes no update path (the domain half of the
two-layer immutability guarantee, REQ-014). The DB trigger is the other
half.

Traceability: REQ-013, REQ-014, REQ-016; BR-005, BR-006, BR-020.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Approval, ArtistIdentityProfileVersion


class AipVersionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def existing_numbers(self, aip_id: uuid.UUID) -> list[int]:
        result = await self._session.execute(
            select(ArtistIdentityProfileVersion.version_number).where(
                ArtistIdentityProfileVersion.aip_id == aip_id
            )
        )
        return list(result.scalars())

    async def create_version(
        self,
        aip_id: uuid.UUID,
        workspace_id: uuid.UUID,
        version_number: int,
        sections: dict,
        created_from_token: int,
        created_by: str,
    ) -> ArtistIdentityProfileVersion:
        version = ArtistIdentityProfileVersion(
            aip_id=aip_id,
            workspace_id=workspace_id,
            version_number=version_number,
            sections=sections,
            created_from_token=created_from_token,
            created_by=created_by,
        )
        self._session.add(version)
        await self._session.flush()
        return version

    async def create_approval(
        self,
        version_id: uuid.UUID,
        actor_id: str,
        note: str | None = None,
    ) -> Approval:
        approval = Approval(
            version_id=version_id, actor_id=actor_id, note=note
        )
        self._session.add(approval)
        await self._session.flush()
        return approval

    async def get_version(
        self, version_id: uuid.UUID
    ) -> ArtistIdentityProfileVersion | None:
        return await self._session.get(ArtistIdentityProfileVersion, version_id)

    async def list_for_aip(
        self, aip_id: uuid.UUID
    ) -> list[ArtistIdentityProfileVersion]:
        result = await self._session.execute(
            select(ArtistIdentityProfileVersion)
            .where(ArtistIdentityProfileVersion.aip_id == aip_id)
            .order_by(ArtistIdentityProfileVersion.version_number)
        )
        return list(result.scalars())

    async def approval_for_version(
        self, version_id: uuid.UUID
    ) -> Approval | None:
        result = await self._session.execute(
            select(Approval).where(Approval.version_id == version_id)
        )
        return result.scalars().first()
