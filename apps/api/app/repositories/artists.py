"""Artist persistence (Phase 5, Increment 5.1).

create() persists the artist and its empty AIP draft in the same
transaction (REQ-003, AC-002): both rows flush together and commit or
roll back as one unit; no code path creates an artist without its AIP.

Traceability: REQ-003, REQ-004; AC-002; BR-001.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Artist, ArtistIdentityProfile


class ArtistRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        workspace_id: uuid.UUID,
        name: str,
        genre: str | None = None,
        summary: str | None = None,
    ) -> Artist:
        artist = Artist(
            workspace_id=workspace_id, name=name, genre=genre, summary=summary
        )
        self._session.add(artist)
        await self._session.flush()
        self._session.add(
            ArtistIdentityProfile(artist_id=artist.id, workspace_id=workspace_id)
        )
        await self._session.flush()
        return artist

    async def get(self, artist_id: uuid.UUID) -> Artist | None:
        return await self._session.get(Artist, artist_id)

    async def get_profile(self, artist_id: uuid.UUID) -> ArtistIdentityProfile | None:
        result = await self._session.execute(
            select(ArtistIdentityProfile).where(
                ArtistIdentityProfile.artist_id == artist_id
            )
        )
        return result.scalar_one_or_none()

    async def list_for_workspace(self, workspace_id: uuid.UUID) -> list[Artist]:
        result = await self._session.execute(
            select(Artist)
            .where(Artist.workspace_id == workspace_id)
            .order_by(Artist.created_at)
        )
        return list(result.scalars())
