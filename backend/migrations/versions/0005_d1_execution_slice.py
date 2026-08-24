"""add durable D1 simulator execution and evidence records

Revision ID: 0005
Revises: 0004
"""

import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "project_id", sa.Uuid(), sa.ForeignKey("projects.id"), nullable=False
        ),
        sa.Column(
            "mission_id", sa.Uuid(), sa.ForeignKey("missions.id"), nullable=False
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("desired_outcome", sa.Text(), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    for name, columns in (
        ("ix_tasks_workspace_id", ["workspace_id"]),
        ("ix_tasks_project_id", ["project_id"]),
        ("ix_tasks_mission_id", ["mission_id"]),
        ("ix_tasks_state", ["state"]),
        ("ix_tasks_created_by", ["created_by"]),
    ):
        op.create_index(name, "tasks", columns)
    op.create_table(
        "task_snapshots",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("task_id", sa.Uuid(), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column("simulator_profile", sa.String(64), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_task_snapshots_task_id", "task_snapshots", ["task_id"])
    op.create_index(
        "ix_task_snapshots_workspace_id", "task_snapshots", ["workspace_id"]
    )
    op.create_table(
        "execution_runs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "project_id", sa.Uuid(), sa.ForeignKey("projects.id"), nullable=False
        ),
        sa.Column(
            "mission_id", sa.Uuid(), sa.ForeignKey("missions.id"), nullable=False
        ),
        sa.Column("task_id", sa.Uuid(), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column(
            "task_snapshot_id",
            sa.Uuid(),
            sa.ForeignKey("task_snapshots.id"),
            nullable=False,
        ),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("state_reason", sa.String(96), nullable=True),
        sa.Column("idempotency_key", sa.String(128), nullable=False),
        sa.Column("request_hash", sa.String(64), nullable=False),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sa.String(128), nullable=False, unique=True),
        sa.Column("cancellation_state", sa.String(32), nullable=False),
        sa.Column("receipt_state", sa.String(32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("last_reliable_evidence_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint(
            "workspace_id",
            "idempotency_key",
            name="uq_execution_runs_workspace_idempotency",
        ),
    )
    for name, columns in (
        ("ix_execution_runs_workspace_id", ["workspace_id"]),
        ("ix_execution_runs_project_id", ["project_id"]),
        ("ix_execution_runs_mission_id", ["mission_id"]),
        ("ix_execution_runs_task_id", ["task_id"]),
        ("ix_execution_runs_task_snapshot_id", ["task_snapshot_id"]),
        ("ix_execution_runs_state", ["state"]),
        ("ix_execution_runs_correlation_id", ["correlation_id"]),
    ):
        op.create_index(name, "execution_runs", columns)
    op.create_table(
        "run_attempts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "run_id", sa.Uuid(), sa.ForeignKey("execution_runs.id"), nullable=False
        ),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(160), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("failure_kind", sa.String(64), nullable=True),
        sa.Column("provider_identity", sa.String(128), nullable=False),
        sa.Column("side_effect_certainty", sa.String(32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("run_id", "attempt_number", name="uq_run_attempts_number"),
    )
    for name, columns in (
        ("ix_run_attempts_run_id", ["run_id"]),
        ("ix_run_attempts_workspace_id", ["workspace_id"]),
        ("ix_run_attempts_state", ["state"]),
    ):
        op.create_index(name, "run_attempts", columns)
    op.create_table(
        "artifacts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "run_id", sa.Uuid(), sa.ForeignKey("execution_runs.id"), nullable=False
        ),
        sa.Column(
            "attempt_id", sa.Uuid(), sa.ForeignKey("run_attempts.id"), nullable=False
        ),
        sa.Column("media_type", sa.String(128), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    for name, columns in (
        ("ix_artifacts_workspace_id", ["workspace_id"]),
        ("ix_artifacts_run_id", ["run_id"]),
        ("ix_artifacts_attempt_id", ["attempt_id"]),
    ):
        op.create_index(name, "artifacts", columns)
    op.create_table(
        "execution_receipts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "run_id",
            sa.Uuid(),
            sa.ForeignKey("execution_runs.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "attempt_id", sa.Uuid(), sa.ForeignKey("run_attempts.id"), nullable=True
        ),
        sa.Column(
            "artifact_id", sa.Uuid(), sa.ForeignKey("artifacts.id"), nullable=True
        ),
        sa.Column("terminal_state", sa.String(32), nullable=False),
        sa.Column("reason_code", sa.String(96), nullable=True),
        sa.Column("simulator_identity", sa.String(128), nullable=False),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column("output_hash", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    for name, columns in (
        ("ix_execution_receipts_workspace_id", ["workspace_id"]),
        ("ix_execution_receipts_attempt_id", ["attempt_id"]),
        ("ix_execution_receipts_artifact_id", ["artifact_id"]),
    ):
        op.create_index(name, "execution_receipts", columns)


def downgrade():
    for name in (
        "ix_execution_receipts_artifact_id",
        "ix_execution_receipts_attempt_id",
        "ix_execution_receipts_workspace_id",
    ):
        op.drop_index(name, table_name="execution_receipts")
    op.drop_table("execution_receipts")
    for name in (
        "ix_artifacts_attempt_id",
        "ix_artifacts_run_id",
        "ix_artifacts_workspace_id",
    ):
        op.drop_index(name, table_name="artifacts")
    op.drop_table("artifacts")
    for name in (
        "ix_run_attempts_state",
        "ix_run_attempts_workspace_id",
        "ix_run_attempts_run_id",
    ):
        op.drop_index(name, table_name="run_attempts")
    op.drop_table("run_attempts")
    for name in (
        "ix_execution_runs_correlation_id",
        "ix_execution_runs_state",
        "ix_execution_runs_task_snapshot_id",
        "ix_execution_runs_task_id",
        "ix_execution_runs_mission_id",
        "ix_execution_runs_project_id",
        "ix_execution_runs_workspace_id",
    ):
        op.drop_index(name, table_name="execution_runs")
    op.drop_table("execution_runs")
    op.drop_index("ix_task_snapshots_workspace_id", table_name="task_snapshots")
    op.drop_index("ix_task_snapshots_task_id", table_name="task_snapshots")
    op.drop_table("task_snapshots")
    for name in (
        "ix_tasks_created_by",
        "ix_tasks_state",
        "ix_tasks_mission_id",
        "ix_tasks_project_id",
        "ix_tasks_workspace_id",
    ):
        op.drop_index(name, table_name="tasks")
    op.drop_table("tasks")
