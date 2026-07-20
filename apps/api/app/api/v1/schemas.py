"""Request and response schemas for the v1 API (Phase 5, Increment 5.2).

Shape validation lives here (422 with field and rule via the shared
validation handler, AC-003); business rules live in the domain services.

Traceability: AC-002, AC-003; D5-1.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


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
