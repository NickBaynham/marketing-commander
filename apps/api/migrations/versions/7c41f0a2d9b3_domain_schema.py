"""Domain schema: users, workspaces, memberships, artists, AIP drafts.

Phase 5, Increment 5.1. The first non-trivial schema: seeded-identity
users, the single workspace, owner membership, artists with lifecycle
state and case-insensitive per-workspace name uniqueness, and the
minimal empty AIP draft record created with each artist (REQ-003,
AC-002).

Revision ID: 7c41f0a2d9b3
Revises: 4e21b456f9ec
"""

import sqlalchemy as sa
from alembic import op

revision = "7c41f0a2d9b3"
down_revision = "4e21b456f9ec"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("display_name", sa.String(120), nullable=False),
        sa.Column(
            "identity_source",
            sa.String(32),
            nullable=False,
            server_default=sa.text("'local_seed'"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_table(
        "workspaces",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column(
            "created_by", sa.String(64), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_table(
        "workspace_memberships",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "workspace_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("workspaces.id"),
            nullable=False,
        ),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column(
            "granted_by", sa.String(64), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "user_id", "workspace_id", name="uq_membership_user_workspace"
        ),
    )
    op.create_table(
        "artists",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("workspaces.id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column(
            "state", sa.String(16), nullable=False, server_default=sa.text("'active'")
        ),
        sa.Column("genre", sa.String(120), nullable=True),
        sa.Column("summary", sa.String(500), nullable=True),
        sa.Column(
            "version_token", sa.Integer, nullable=False, server_default=sa.text("1")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "uq_artist_workspace_name_ci",
        "artists",
        ["workspace_id", sa.text("lower(name)")],
        unique=True,
    )
    op.create_table(
        "artist_identity_profiles",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "artist_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "workspace_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("workspaces.id"),
            nullable=False,
        ),
        sa.Column(
            "version_token", sa.Integer, nullable=False, server_default=sa.text("1")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("artist_identity_profiles")
    op.drop_index("uq_artist_workspace_name_ci", table_name="artists")
    op.drop_table("artists")
    op.drop_table("workspace_memberships")
    op.drop_table("workspaces")
    op.drop_table("users")
