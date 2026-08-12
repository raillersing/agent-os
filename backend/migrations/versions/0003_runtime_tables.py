"""add agent runtime tables managed by Alembic

Revision ID: 0003
Revises: 0002
"""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agents",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("capabilities", sa.JSON(), nullable=True),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("policies", sa.JSON(), nullable=True),
        sa.Column("total_runs", sa.Integer(), nullable=True),
        sa.Column("successful_runs", sa.Integer(), nullable=True),
        sa.Column("failed_runs", sa.Integer(), nullable=True),
        sa.Column("total_tokens", sa.BigInteger(), nullable=True),
        sa.Column("total_cost", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_agents_name", "agents", ["name"])
    op.create_index("ix_agents_status", "agents", ["status"])

    op.create_table(
        "memory",
        sa.Column("key", sa.String(255), primary_key=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("type", sa.String(50), nullable=True),
        sa.Column("source", sa.String(255), nullable=True),
        sa.Column("agent_id", sa.Uuid(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("embedding_id", sa.String(255), nullable=True),
        sa.Column("access_count", sa.Integer(), nullable=True),
        sa.Column("last_accessed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_memory_type", "memory", ["type"])
    op.create_index("ix_memory_agent_id", "memory", ["agent_id"])

    op.create_table(
        "runs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("agent_id", sa.Uuid(), sa.ForeignKey("agents.id"), nullable=False),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("context", sa.JSON(), nullable=True),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("progress", sa.Integer(), nullable=True),
        sa.Column("current_step", sa.String(255), nullable=True),
        sa.Column("steps", sa.JSON(), nullable=True),
        sa.Column("tokens_used", sa.Integer(), nullable=True),
        sa.Column("cost", sa.Float(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_runs_agent_id", "runs", ["agent_id"])
    op.create_index("ix_runs_status", "runs", ["status"])


def downgrade():
    op.drop_index("ix_runs_status", table_name="runs")
    op.drop_index("ix_runs_agent_id", table_name="runs")
    op.drop_table("runs")
    op.drop_index("ix_memory_agent_id", table_name="memory")
    op.drop_index("ix_memory_type", table_name="memory")
    op.drop_table("memory")
    op.drop_index("ix_agents_status", table_name="agents")
    op.drop_index("ix_agents_name", table_name="agents")
    op.drop_table("agents")
