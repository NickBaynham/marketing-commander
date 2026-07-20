"""Audit records: append-only trail with non-null actor (BR-020, REQ-040).

Phase 5, Increment 5.2.

Revision ID: 9d2e8b1c4f70
Revises: 7c41f0a2d9b3
"""

import sqlalchemy as sa
from alembic import op

revision = "9d2e8b1c4f70"
down_revision = "7c41f0a2d9b3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_records",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_id", sa.String(64), nullable=False),
        sa.Column("action", sa.String(64), nullable=False),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_audit_entity", "audit_records", ["entity_type", "entity_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_audit_entity", table_name="audit_records")
    op.drop_table("audit_records")
