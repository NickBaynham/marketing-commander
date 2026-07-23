"""Request and response schemas for the v1 API (Phase 5, Increment 5.2).

Shape validation lives here (422 with field and rule via the shared
validation handler, AC-003); business rules live in the domain services.

Traceability: AC-002, AC-003; D5-1.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.aip import AipSections


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class WorkspaceOut(BaseModel):
    id: uuid.UUID
    name: str
    created_by: str
    created: bool = False

    model_config = {"from_attributes": True}


class ArtistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    genre: str | None = Field(default=None, max_length=120)
    summary: str | None = Field(default=None, max_length=500)


class ArtistUpdate(BaseModel):
    expected_version: int
    name: str | None = Field(default=None, min_length=1, max_length=120)
    genre: str | None = Field(default=None, max_length=120)
    summary: str | None = Field(default=None, max_length=500)


class VersionedAction(BaseModel):
    expected_version: int


class ArtistOut(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str
    state: str
    genre: str | None
    summary: str | None
    version_token: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DeletionOut(BaseModel):
    removed: dict[str, str]


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=1024)


class MeOut(BaseModel):
    user_id: str


class ApproveRequest(BaseModel):
    expected_version: int
    note: str | None = Field(default=None, max_length=2000)


class AipVersionOut(BaseModel):
    id: uuid.UUID
    artist_id: uuid.UUID
    version_number: int
    version_label: str
    status: str
    created_at: datetime
    created_by: str
    approved_by: str | None
    approved_at: datetime | None


class AipVersionExportOut(BaseModel):
    markdown: str


class AipDraftSave(BaseModel):
    """Explicit save (SCR-07). Per-section content caps (DEC-09) are
    enforced by AipSections at this boundary → 422 in the AC-003 shape;
    total-size and version conflicts are handled by the domain service."""

    expected_version: int
    sections: AipSections


class AipDraftView(BaseModel):
    """Draft state for SCR-07/SCR-08: sections plus derived completeness,
    eligibility, and the exact blocking list."""

    artist_id: uuid.UUID
    version_token: int
    sections: AipSections
    completeness: float
    display_percentage: float
    approval_eligible: bool
    incomplete_required_sections: list[str]


class AipPreviewOut(BaseModel):
    markdown: str
