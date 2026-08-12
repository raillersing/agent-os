"""add workspace audit events

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-30
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False),
        sa.Column("event_type", sa.String(96), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.Uuid(), nullable=False),
        sa.Column("actor", sa.String(128), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_audit_events_workspace_id", "audit_events", ["workspace_id"])
    op.create_index("ix_audit_events_event_type", "audit_events", ["event_type"])
    op.create_index("ix_audit_events_resource_id", "audit_events", ["resource_id"])
    op.create_index("ix_audit_events_created_at", "audit_events", ["created_at"])


def downgrade():
    op.drop_index("ix_audit_events_created_at", table_name="audit_events")
    op.drop_index("ix_audit_events_resource_id", table_name="audit_events")
    op.drop_index("ix_audit_events_event_type", table_name="audit_events")
    op.drop_index("ix_audit_events_workspace_id", table_name="audit_events")
    op.drop_table("audit_events")
