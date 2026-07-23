"""AIP approval domain service (Phase 7, Increment 7.2).

Owns the policy: gate approval on DEC-02 eligibility (reusing the
completeness engine), enforce the draft version token, snapshot the
eligible draft into an immutable version (numbered by the version
domain), record the Approval with a non-null actor, and audit with
correlation. Collaborators are injected by transport wiring; this module
imports neither transport nor persistence.

Traceability: REQ-010, REQ-013, REQ-015, REQ-016; AC-006, AC-007;
BR-004, BR-005, BR-006, BR-020; DEC-02, DEC-03; D7-2, D7-4, D7-6.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime

from app.correlation import get_correlation_id
from app.domain.aip import AipSections, approval_eligible, incomplete_required_sections
from app.domain.aip import render_markdown
from app.domain.aip_versions import derived_status, next_version_number, version_label
from app.exceptions import ApprovalNotEligible, NotFound, StaleVersion


@dataclass(frozen=True)
class VersionView:
    id: uuid.UUID
    artist_id: uuid.UUID
    version_number: int
    version_label: str
    status: str
    created_at: datetime
    created_by: str
    approved_by: str | None
    approved_at: datetime | None


class AipApprovalService:
    def __init__(self, aip, versions, audit, actor_id: str) -> None:
        self._aip = aip
        self._versions = versions
        self._audit = audit
        self._actor_id = actor_id

    def _view(self, version, artist_id, approval, numbers: list[int]) -> VersionView:
        return VersionView(
            id=version.id,
            artist_id=artist_id,
            version_number=version.version_number,
            version_label=version_label(version.version_number),
            status=derived_status(version.version_number, numbers),
            created_at=version.created_at,
            created_by=version.created_by,
            approved_by=approval.actor_id if approval else None,
            approved_at=approval.created_at if approval else None,
        )

    async def approve(
        self, artist_id: uuid.UUID, expected_version: int, note: str | None = None
    ) -> VersionView:
        profile = await self._aip.get(artist_id)
        if profile is None:
            raise NotFound("artist identity profile")
        if profile.version_token != expected_version:
            raise StaleVersion(
                f"expected version {expected_version}, "
                f"current is {profile.version_token}"
            )
        sections = AipSections.model_validate(profile.sections or {})
        if not approval_eligible(sections):
            raise ApprovalNotEligible(incomplete_required_sections(sections))
        existing = await self._versions.existing_numbers(profile.id)
        number = next_version_number(existing)
        version = await self._versions.create_version(
            aip_id=profile.id,
            workspace_id=profile.workspace_id,
            version_number=number,
            sections=dict(profile.sections),
            created_from_token=profile.version_token,
            created_by=self._actor_id,
        )
        approval = await self._versions.create_approval(
            version.id, self._actor_id, note
        )
        await self._audit.record(
            actor_id=self._actor_id,
            action="aip.approved",
            entity_type="aip_version",
            entity_id=str(version.id),
            correlation_id=get_correlation_id(),
        )
        return self._view(version, artist_id, approval, [*existing, number])

    async def list_versions(self, artist_id: uuid.UUID) -> list[VersionView]:
        profile = await self._aip.get(artist_id)
        if profile is None:
            raise NotFound("artist identity profile")
        versions = await self._versions.list_for_aip(profile.id)
        numbers = [v.version_number for v in versions]
        views = []
        for version in versions:
            approval = await self._versions.approval_for_version(version.id)
            views.append(self._view(version, artist_id, approval, numbers))
        return views

    async def get_version(self, version_id: uuid.UUID) -> VersionView:
        version = await self._versions.get_version(version_id)
        if version is None:
            raise NotFound("AIP version")
        ref = await self._versions.artist_ref_for_aip(version.aip_id)
        numbers = await self._versions.existing_numbers(version.aip_id)
        approval = await self._versions.approval_for_version(version.id)
        artist_id = ref[0] if ref else version.aip_id
        return self._view(version, artist_id, approval, numbers)

    async def export_markdown(self, version_id: uuid.UUID) -> str:
        version = await self._versions.get_version(version_id)
        if version is None:
            raise NotFound("AIP version")
        ref = await self._versions.artist_ref_for_aip(version.aip_id)
        name = ref[1] if ref else "Unknown artist"
        sections = AipSections.model_validate(version.sections)
        return render_markdown(name, sections)
