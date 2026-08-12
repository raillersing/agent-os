"""persistent control plane baseline

Revision ID: 0001
Revises:
Create Date: 2026-07-28
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # The development app currently creates the same baseline through metadata
    # for a zero-setup local start. Alembic owns subsequent production upgrades.
    op.create_table(
        "workspaces",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("budget", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_workspaces_status", "workspaces", ["status"])
    op.create_table(
        "missions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("plan", sa.JSON(), nullable=True),
        sa.Column("evidence", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_missions_workspace_id", "missions", ["workspace_id"])
    op.create_index("ix_missions_status", "missions", ["status"])
    op.create_table(
        "automations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("trigger_type", sa.String(64), nullable=False),
        sa.Column("trigger_config", sa.JSON(), nullable=True),
        sa.Column("steps", sa.JSON(), nullable=True),
        sa.Column("enabled", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_automations_workspace_id", "automations", ["workspace_id"])
    op.create_table(
        "approvals",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "mission_id", sa.Uuid(), sa.ForeignKey("missions.id"), nullable=False
        ),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("scope", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("decided_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_approvals_mission_id", "approvals", ["mission_id"])
    op.create_index("ix_approvals_status", "approvals", ["status"])


def downgrade():
    op.drop_index("ix_approvals_status", table_name="approvals")
    op.drop_index("ix_approvals_mission_id", table_name="approvals")
    op.drop_table("approvals")
    op.drop_index("ix_automations_workspace_id", table_name="automations")
    op.drop_table("automations")
    op.drop_index("ix_missions_status", table_name="missions")
    op.drop_index("ix_missions_workspace_id", table_name="missions")
    op.drop_table("missions")
    op.drop_index("ix_workspaces_status", table_name="workspaces")
    op.drop_table("workspaces")
