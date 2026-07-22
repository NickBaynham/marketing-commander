"""AIP draft domain service (Phase 6, Increment 6.2).

Owns the policy: parse and validate sections against the typed schema
and DEC-09 size limits, explicit save under optimistic concurrency
(BR-019), audit with correlation on every save (B4 lesson), and Markdown
preview rendering. Collaborators (AIP repository, audit recorder) are
injected by transport wiring; this module imports neither transport nor
persistence.

Traceability: REQ-006..REQ-012, REQ-045; AC-004, AC-005, AC-008;
BR-002, BR-003, BR-019, BR-020; DEC-02, DEC-09; D6-1.
"""

import uuid
from dataclasses import dataclass

from app.correlation import get_correlation_id
from app.domain.aip import (
    AipSections,
    approval_eligible,
    completeness,
    display_percentage,
    incomplete_required_sections,
    render_markdown,
    size_violations,
)
from app.exceptions import NotFound, StaleVersion, ValidationFailed


@dataclass(frozen=True)
class AipDraftState:
    artist_id: uuid.UUID
    version_token: int
    sections: AipSections
    completeness: float
    display_percentage: float
    approval_eligible: bool
    incomplete_required_sections: list[str]


class AipService:
    def __init__(self, aip, audit, actor_id: str) -> None:
        self._aip = aip
        self._audit = audit
        self._actor_id = actor_id

    async def _require(self, artist_id: uuid.UUID):
        profile = await self._aip.get(artist_id)
        if profile is None:
            raise NotFound("artist identity profile")
        return profile

    def _state(self, profile, sections: AipSections) -> AipDraftState:
        return AipDraftState(
            artist_id=profile.artist_id,
            version_token=profile.version_token,
            sections=sections,
            completeness=completeness(sections),
            display_percentage=display_percentage(sections),
            approval_eligible=approval_eligible(sections),
            incomplete_required_sections=incomplete_required_sections(sections),
        )

    async def get_draft(self, artist_id: uuid.UUID) -> AipDraftState:
        profile = await self._require(artist_id)
        sections = AipSections.model_validate(profile.sections or {})
        return self._state(profile, sections)

    async def save_draft(
        self,
        artist_id: uuid.UUID,
        expected_version: int,
        sections: AipSections,
    ) -> AipDraftState:
        profile = await self._require(artist_id)
        # Friendly pre-check; the real guarantee is the version-conditioned
        # UPDATE in the repository (StaleDataError -> StaleVersion).
        if profile.version_token != expected_version:
            raise StaleVersion(
                f"expected version {expected_version}, "
                f"current is {profile.version_token}"
            )
        violations = size_violations(sections)
        if violations:
            first = violations[0]
            raise ValidationFailed(first["field"], first["rule"], first["message"])
        profile.sections = sections.model_dump(mode="json")
        await self._aip.save(profile)
        await self._audit.record(
            actor_id=self._actor_id,
            action="aip.saved",
            entity_type="artist_identity_profile",
            entity_id=str(artist_id),
            correlation_id=get_correlation_id(),
        )
        return self._state(profile, sections)

    async def preview(self, artist_id: uuid.UUID) -> str:
        profile = await self._require(artist_id)
        sections = AipSections.model_validate(profile.sections or {})
        name = await self._aip.artist_name(artist_id) or "Unknown artist"
        return render_markdown(name, sections)
