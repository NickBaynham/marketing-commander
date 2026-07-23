"""Persisted domain records (Phase 5, Increment 5.1).

Shared persistence-shaped records, importable by any layer like app.db
and app.config (the layering rule keeps *logic* out of the wrong layers;
these classes carry no behavior). Identifiers are application-generated
UUIDv7 (domain model conventions); every owned aggregate carries
workspace_id (BR-001); mutable aggregates carry a version token for
optimistic concurrency (BR-019).

The ArtistIdentityProfile here is the minimal empty-draft record created
with the artist (REQ-003, AC-002). Section schema, statuses, and the
editor arrive in Phase 6.

Traceability: REQ-001..REQ-005, REQ-051 (schema), BR-001, BR-014,
BR-019, BR-020; domain model v1.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

ARTIST_STATES = ("active", "archived")


def uuid7() -> uuid.UUID:
    return uuid.uuid7()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class User(TimestampMixin, Base):
    """A human identity; the MVP seeds exactly one (`local-owner`, DEC-03)."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    identity_source: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default=text("'local_seed'")
    )


class Workspace(TimestampMixin, Base):
    """Ownership, authorization, budget, and data-isolation boundary (DEC-01)."""

    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_by: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )


class WorkspaceMembership(TimestampMixin, Base):
    """Links a user to a workspace with a role; unique per (user, workspace)."""

    __tablename__ = "workspace_memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "workspace_id", name="uq_membership_user_workspace"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    granted_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)


class Artist(TimestampMixin, Base):
    """The marketed artist; name unique (case-insensitive) per workspace."""

    __tablename__ = "artists"
    __table_args__ = (
        Index(
            "uq_artist_workspace_name_ci",
            "workspace_id",
            func.lower(text("name")),
            unique=True,
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default=text("'active'")
    )
    genre: Mapped[str | None] = mapped_column(String(120))
    summary: Mapped[str | None] = mapped_column(String(500))
    version_token: Mapped[int] = mapped_column(
        nullable=False, server_default=text("1")
    )

    # BR-019 for real concurrency: SQLAlchemy conditions every UPDATE and
    # DELETE on the loaded version (WHERE id = ... AND version_token = ...)
    # and raises StaleDataError on a lost race — check-then-write alone
    # cannot prevent silent overwrites under READ COMMITTED.
    __mapper_args__ = {"version_id_col": version_token}


class AuditRecord(Base):
    """Append-only audit trail: every state change names its actor
    (BR-020, REQ-040)."""

    __tablename__ = "audit_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    actor_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ArtistIdentityProfile(TimestampMixin, Base):
    """AIP draft, created empty with its artist (REQ-003, AC-002).

    One per artist. `sections` holds the twelve-section JSONB document
    (DEC-02, D6-1) validated by the typed schema in app/domain/aip.py;
    completeness and eligibility are always derived, never stored
    (BR-002).
    """

    __tablename__ = "artist_identity_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    artist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id"), nullable=False
    )
    version_token: Mapped[int] = mapped_column(
        nullable=False, server_default=text("1")
    )
    sections: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )

    # BR-019 (B1 lesson): every UPDATE is conditioned on the loaded
    # version_token; a losing concurrent save raises StaleDataError
    # instead of silently overwriting the winner's edit.
    __mapper_args__ = {"version_id_col": version_token}


class ArtistIdentityProfileVersion(Base):
    """Immutable approved AIP snapshot (Phase 7, REQ-013).

    Insert-only: no updatable columns, no version token. A BEFORE UPDATE
    trigger blocks mutation for the application role (REQ-014, ADR-005,
    D7-3). Active authority is derived — the highest version_number is
    active, older ones are superseded — never a stored mutation (D7-2).
    """

    __tablename__ = "artist_identity_profile_versions"
    __table_args__ = (
        UniqueConstraint(
            "aip_id", "version_number", name="uq_aip_version_number"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    aip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("artist_identity_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(nullable=False)
    sections: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # The draft version_token this snapshot was taken from (provenance).
    created_from_token: Mapped[int] = mapped_column(nullable=False)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Approval(Base):
    """Immutable record of an actor accepting one exact version
    (REQ-016, BR-020). Insert-only; a BEFORE UPDATE trigger blocks
    mutation. `context`/`batch_id` carry the individual-vs-bulk shape;
    bulk is unused until Phase 12 (DEC-08)."""

    __tablename__ = "approvals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid7
    )
    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("artist_identity_profile_versions.id", ondelete="CASCADE"),
        nullable=False,
    )
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    context: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default=text("'individual'")
    )
    batch_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    note: Mapped[str | None] = mapped_column(String(2000))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
