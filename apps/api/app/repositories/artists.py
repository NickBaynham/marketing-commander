"""Artist persistence (Phase 5, Increment 5.1).

create() persists the artist and its empty AIP draft in the same
transaction (REQ-003, AC-002): both rows flush together and commit or
roll back as one unit; no code path creates an artist without its AIP.

Traceability: REQ-003, REQ-004; AC-002; BR-001.
"""

import uuid

from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from app.exceptions import DuplicateArtistName, StaleVersion
from app.models import Artist, ArtistIdentityProfile

UNIQUE_NAME_INDEX = "uq_artist_workspace_name_ci"


def _is_duplicate_name(exc: IntegrityError) -> bool:
    # asyncpg exposes the violated constraint structurally; fall back to
    # the message only if the attribute is absent.
    constraint = getattr(exc.orig, "constraint_name", None)
    if constraint is not None:
        return constraint == UNIQUE_NAME_INDEX
    return UNIQUE_NAME_INDEX in str(exc.orig)


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
        try:
            await self._session.flush()
        except IntegrityError as exc:
            if _is_duplicate_name(exc):
                raise DuplicateArtistName(name) from exc
            raise
        self._session.add(
            ArtistIdentityProfile(artist_id=artist.id, workspace_id=workspace_id)
        )
        await self._session.flush()
        return artist

    async def save(self, artist: Artist) -> Artist:
        try:
            await self._session.flush()
        except IntegrityError as exc:
            if _is_duplicate_name(exc):
                raise DuplicateArtistName(artist.name) from exc
            raise
        except StaleDataError as exc:
            # The versioned UPDATE matched no row: a concurrent writer got
            # there first (BR-019 — no silent overwrite).
            raise StaleVersion(
                "a concurrent update changed this artist; reload and retry"
            ) from exc
        return artist

    async def delete(self, artist: Artist) -> dict[str, str]:
        """Remove the artist aggregate; the AIP draft cascades. Returns
        what was removed so the response can name the loss (BR-015)."""
        removed = {"artist": artist.name, "aip_draft": "empty draft"}
        await self._session.execute(
            sa_delete(ArtistIdentityProfile).where(
                ArtistIdentityProfile.artist_id == artist.id
            )
        )
        await self._session.delete(artist)
        await self._session.flush()
        return removed

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
