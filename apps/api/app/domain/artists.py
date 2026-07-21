"""Artist domain service (Phase 5, Increment 5.2).

Owns the policy: validation rules (D5-1), lifecycle transitions
(BR-014), optimistic concurrency (BR-019), confirmed deletion (BR-015),
and audit on every state change (BR-020). Collaborators (artist
repository, audit recorder) are injected by transport wiring; this
module imports neither transport nor persistence.

Authorization note (documented limitation, Phase 8): the single seeded
local owner is the only actor; real access control arrives in Phase 8.

Traceability: REQ-003, REQ-004, REQ-005, REQ-051; AC-002, AC-003,
AC-025; BR-014, BR-015, BR-019, BR-020; D5-1.
"""

import uuid

from app.correlation import get_correlation_id
from app.exceptions import (
    ArtistArchived,
    NotFound,
    StaleVersion,
    ValidationFailed,
)

NAME_MIN, NAME_MAX = 1, 120
GENRE_MAX, SUMMARY_MAX = 120, 500


def _validated_name(name: str) -> str:
    trimmed = name.strip()
    if not (NAME_MIN <= len(trimmed) <= NAME_MAX):
        raise ValidationFailed(
            "name",
            "length",
            f"name must be {NAME_MIN}-{NAME_MAX} characters after trimming",
        )
    return trimmed


class ArtistService:
    def __init__(self, artists, audit, actor_id: str) -> None:
        self._artists = artists
        self._audit = audit
        self._actor_id = actor_id

    async def _audited(self, action: str, entity_id: uuid.UUID) -> None:
        await self._audit.record(
            actor_id=self._actor_id,
            action=action,
            entity_type="artist",
            entity_id=str(entity_id),
            correlation_id=get_correlation_id(),
        )

    async def create(
        self,
        workspace_id: uuid.UUID,
        name: str,
        genre: str | None = None,
        summary: str | None = None,
    ):
        artist = await self._artists.create(
            workspace_id=workspace_id,
            name=_validated_name(name),
            genre=genre,
            summary=summary,
        )
        await self._audited("artist.created", artist.id)
        return artist

    async def get(self, artist_id: uuid.UUID):
        artist = await self._artists.get(artist_id)
        if artist is None:
            raise NotFound("artist")
        return artist

    async def list_for_workspace(self, workspace_id: uuid.UUID):
        return await self._artists.list_for_workspace(workspace_id)

    async def get_profile(self, artist_id: uuid.UUID):
        await self.get(artist_id)
        return await self._artists.get_profile(artist_id)

    def _check_version(self, artist, expected_version: int) -> None:
        if artist.version_token != expected_version:
            raise StaleVersion(
                f"expected version {expected_version}, "
                f"current is {artist.version_token}"
            )

    async def update(
        self,
        artist_id: uuid.UUID,
        expected_version: int,
        name: str | None = None,
        genre: str | None = None,
        summary: str | None = None,
    ):
        artist = await self.get(artist_id)
        if artist.state == "archived":
            raise ArtistArchived("archived artists are read-only (BR-014)")
        self._check_version(artist, expected_version)
        if name is not None:
            artist.name = _validated_name(name)
        if genre is not None:
            artist.genre = genre
        if summary is not None:
            artist.summary = summary
        # version_token increments via the mapper's version counter on
        # flush (models.Artist.__mapper_args__), which also conditions the
        # UPDATE on the loaded version — the real BR-019 guarantee.
        await self._artists.save(artist)
        await self._audited("artist.updated", artist.id)
        return artist

    async def archive(self, artist_id: uuid.UUID, expected_version: int):
        artist = await self.get(artist_id)
        if artist.state == "archived":
            return artist
        self._check_version(artist, expected_version)
        artist.state = "archived"
        await self._artists.save(artist)
        await self._audited("artist.archived", artist.id)
        return artist

    async def restore(self, artist_id: uuid.UUID, expected_version: int):
        artist = await self.get(artist_id)
        if artist.state == "active":
            return artist
        self._check_version(artist, expected_version)
        artist.state = "active"
        await self._artists.save(artist)
        await self._audited("artist.restored", artist.id)
        return artist

    async def delete(self, artist_id: uuid.UUID, confirm_name: str | None) -> dict:
        """BR-015/REQ-051: the confirmation must prove foreknowledge of the
        loss — the caller names the artist being destroyed."""
        artist = await self.get(artist_id)
        if confirm_name is None or confirm_name.strip() != artist.name:
            raise ValidationFailed(
                "confirm_name",
                "must_match_artist_name",
                f'deletion permanently removes the artist "{artist.name}" '
                "and its identity profile draft; confirm by supplying "
                "confirm_name matching the artist name exactly (BR-015)",
            )
        artist_id_value = artist.id
        removed = await self._artists.delete(artist)
        await self._audited("artist.deleted", artist_id_value)
        return removed
