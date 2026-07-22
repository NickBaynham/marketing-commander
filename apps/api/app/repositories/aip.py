"""AIP draft persistence (Phase 6, Increment 6.2).

Loads and saves the single AIP draft per artist. `save` relies on the
model's version_id_col: a concurrent write raises StaleDataError, which
becomes StaleVersion here (BR-019, no silent overwrite).

Traceability: REQ-006, REQ-007; BR-019; D6-1.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from app.exceptions import StaleVersion
from app.models import Artist, ArtistIdentityProfile


class AipRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, artist_id: uuid.UUID) -> ArtistIdentityProfile | None:
        result = await self._session.execute(
            select(ArtistIdentityProfile).where(
                ArtistIdentityProfile.artist_id == artist_id
            )
        )
        return result.scalar_one_or_none()

    async def artist_name(self, artist_id: uuid.UUID) -> str | None:
        result = await self._session.execute(
            select(Artist.name).where(Artist.id == artist_id)
        )
        return result.scalar_one_or_none()

    async def save(self, profile: ArtistIdentityProfile) -> ArtistIdentityProfile:
        try:
            await self._session.flush()
        except StaleDataError as exc:
            raise StaleVersion(
                "a concurrent update changed this draft; reload and retry"
            ) from exc
        return profile
