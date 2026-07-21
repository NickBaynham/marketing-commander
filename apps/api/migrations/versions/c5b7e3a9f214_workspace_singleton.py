"""Workspace singleton index: at most one workspace row (DEC-01).

A unique index over a constant expression makes the single-workspace
invariant a database guarantee instead of an application convention, so
concurrent first-run creations cannot produce two workspaces (REQ-001;
Test Commander Phase 5 review finding B2).

Revision ID: c5b7e3a9f214
Revises: 9d2e8b1c4f70
"""

from alembic import op

revision = "c5b7e3a9f214"
down_revision = "9d2e8b1c4f70"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "CREATE UNIQUE INDEX uq_workspaces_singleton ON workspaces ((true))"
    )


def downgrade() -> None:
    op.execute("DROP INDEX uq_workspaces_singleton")
