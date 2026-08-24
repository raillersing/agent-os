"""add D2 provider, context, usage and evaluation evidence

Revision ID: 0006
Revises: 0005
"""

import sqlalchemy as sa
from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "task_snapshots",
        sa.Column(
            "execution_mode", sa.String(32), nullable=False, server_default="simulator"
        ),
    )
    op.add_column(
        "task_snapshots",
        sa.Column(
            "model_profile",
            sa.String(128),
            nullable=False,
            server_default="model.general.balanced",
        ),
    )

    op.add_column(
        "run_attempts", sa.Column("adapter_id", sa.String(128), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("adapter_version", sa.String(64), nullable=True)
    )
    op.add_column(
        "run_attempts",
        sa.Column("logical_model_profile", sa.String(128), nullable=True),
    )
    op.add_column(
        "run_attempts", sa.Column("configured_provider", sa.String(64), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("configured_model", sa.String(128), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("actual_provider", sa.String(64), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("actual_model", sa.String(128), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("actual_identity_state", sa.String(32), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("context_manifest_id", sa.Uuid(), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("provider_request_id", sa.String(256), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("response_id", sa.String(256), nullable=True)
    )
    op.add_column(
        "run_attempts", sa.Column("usage_source", sa.String(32), nullable=True)
    )
    for name in (
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cached_input_tokens",
    ):
        op.add_column("run_attempts", sa.Column(name, sa.Integer(), nullable=True))
    op.add_column("run_attempts", sa.Column("cost_state", sa.String(32), nullable=True))
    op.add_column("run_attempts", sa.Column("cost_amount", sa.Float(), nullable=True))
    op.add_column("run_attempts", sa.Column("latency_ms", sa.Integer(), nullable=True))
    op.add_column(
        "run_attempts", sa.Column("terminal_reason", sa.String(64), nullable=True)
    )
    op.add_column(
        "execution_receipts",
        sa.Column("provider_identity", sa.String(128), nullable=True),
    )

    op.create_table(
        "context_manifests",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "run_id", sa.Uuid(), sa.ForeignKey("execution_runs.id"), nullable=False
        ),
        sa.Column(
            "attempt_id", sa.Uuid(), sa.ForeignKey("run_attempts.id"), nullable=True
        ),
        sa.Column("context_profile_id", sa.String(128), nullable=False),
        sa.Column("context_profile_version", sa.String(64), nullable=False),
        sa.Column("segments", sa.JSON(), nullable=False),
        sa.Column("system_instruction_hash", sa.String(64), nullable=False),
        sa.Column("rendered_input_hash", sa.String(64), nullable=False),
        sa.Column("manifest_hash", sa.String(64), nullable=False),
        sa.Column("disclosure_state", sa.String(64), nullable=False),
        sa.Column("token_budget", sa.JSON(), nullable=False),
        sa.Column("transformations", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    for name, columns in (
        ("ix_context_manifests_workspace_id", ["workspace_id"]),
        ("ix_context_manifests_run_id", ["run_id"]),
        ("ix_context_manifests_attempt_id", ["attempt_id"]),
    ):
        op.create_index(name, "context_manifests", columns)

    op.create_table(
        "model_invocations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "run_id", sa.Uuid(), sa.ForeignKey("execution_runs.id"), nullable=False
        ),
        sa.Column(
            "attempt_id",
            sa.Uuid(),
            sa.ForeignKey("run_attempts.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "context_manifest_id",
            sa.Uuid(),
            sa.ForeignKey("context_manifests.id"),
            nullable=False,
        ),
        sa.Column("adapter_id", sa.String(128), nullable=False),
        sa.Column("adapter_version", sa.String(64), nullable=False),
        sa.Column("logical_model_profile", sa.String(128), nullable=False),
        sa.Column("configured_provider", sa.String(64), nullable=False),
        sa.Column("configured_model", sa.String(128), nullable=False),
        sa.Column("actual_provider", sa.String(64), nullable=True),
        sa.Column("actual_model", sa.String(128), nullable=True),
        sa.Column("identity_state", sa.String(32), nullable=False),
        sa.Column("provider_request_id", sa.String(256), nullable=True),
        sa.Column("response_id", sa.String(256), nullable=True),
        sa.Column("prompt_hash", sa.String(64), nullable=False),
        sa.Column("runtime_version", sa.String(64), nullable=False),
        sa.Column("workflow_version", sa.String(64), nullable=False),
        sa.Column("policy_version", sa.String(64), nullable=False),
        sa.Column(
            "invocation_state", sa.String(32), nullable=False, server_default="prepared"
        ),
        sa.Column("error_code", sa.String(96), nullable=True),
        sa.Column("stop_reason", sa.String(64), nullable=False),
        sa.Column("refusal_state", sa.String(32), nullable=False),
        sa.Column("tools_enabled", sa.Integer(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_model_invocations_workspace_id", "model_invocations", ["workspace_id"]
    )
    op.create_index("ix_model_invocations_run_id", "model_invocations", ["run_id"])
    op.create_index(
        "ix_context_manifests_manifest_hash", "context_manifests", ["manifest_hash"]
    )

    op.create_table(
        "usage_records",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column(
            "run_id", sa.Uuid(), sa.ForeignKey("execution_runs.id"), nullable=False
        ),
        sa.Column(
            "attempt_id",
            sa.Uuid(),
            sa.ForeignKey("run_attempts.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("source", sa.String(32), nullable=False),
        sa.Column("completeness", sa.String(32), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("total_tokens", sa.Integer(), nullable=True),
        sa.Column("cached_input_tokens", sa.Integer(), nullable=True),
        sa.Column("raw_usage", sa.JSON(), nullable=False),
        sa.Column("pricing_profile_version", sa.String(64), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False),
        sa.Column("cost_state", sa.String(32), nullable=False),
        sa.Column("estimated_cost", sa.Float(), nullable=True),
        sa.Column("measured_cost", sa.Float(), nullable=True),
        sa.Column("provider_reported_cost", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_usage_records_workspace_id", "usage_records", ["workspace_id"])
    op.create_index("ix_usage_records_run_id", "usage_records", ["run_id"])

    op.create_table(
        "evaluation_case_results",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("suite_id", sa.String(128), nullable=False),
        sa.Column("suite_version", sa.String(64), nullable=False),
        sa.Column("case_id", sa.String(128), nullable=False),
        sa.Column(
            "run_id", sa.Uuid(), sa.ForeignKey("execution_runs.id"), nullable=True
        ),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("outcome", sa.String(32), nullable=False),
        sa.Column("dimensions", sa.JSON(), nullable=False),
        sa.Column("threshold_snapshot", sa.JSON(), nullable=False),
        sa.Column("evidence_reference", sa.String(256), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_evaluation_case_results_suite_id", "evaluation_case_results", ["suite_id"]
    )
    op.create_index(
        "ix_evaluation_case_results_case_id", "evaluation_case_results", ["case_id"]
    )
    op.create_index(
        "ix_evaluation_case_results_run_id", "evaluation_case_results", ["run_id"]
    )


def downgrade():
    for name, table in (
        ("ix_evaluation_case_results_run_id", "evaluation_case_results"),
        ("ix_evaluation_case_results_case_id", "evaluation_case_results"),
        ("ix_evaluation_case_results_suite_id", "evaluation_case_results"),
    ):
        op.drop_index(name, table_name=table)
    op.drop_table("evaluation_case_results")
    for name, table in (
        ("ix_usage_records_run_id", "usage_records"),
        ("ix_usage_records_workspace_id", "usage_records"),
    ):
        op.drop_index(name, table_name=table)
    op.drop_table("usage_records")
    for name, table in (
        ("ix_model_invocations_run_id", "model_invocations"),
        ("ix_model_invocations_workspace_id", "model_invocations"),
    ):
        op.drop_index(name, table_name=table)
    op.drop_table("model_invocations")
    for name in (
        "ix_context_manifests_attempt_id",
        "ix_context_manifests_run_id",
        "ix_context_manifests_workspace_id",
        "ix_context_manifests_manifest_hash",
    ):
        op.drop_index(name, table_name="context_manifests")
    op.drop_table("context_manifests")
    op.drop_column("execution_receipts", "provider_identity")
    for name in (
        "terminal_reason",
        "latency_ms",
        "cost_amount",
        "cost_state",
        "cached_input_tokens",
        "total_tokens",
        "output_tokens",
        "input_tokens",
        "usage_source",
        "response_id",
        "provider_request_id",
        "context_manifest_id",
        "actual_identity_state",
        "actual_model",
        "actual_provider",
        "configured_model",
        "configured_provider",
        "logical_model_profile",
        "adapter_version",
        "adapter_id",
    ):
        op.drop_column("run_attempts", name)
    op.drop_column("task_snapshots", "model_profile")
    op.drop_column("task_snapshots", "execution_mode")
