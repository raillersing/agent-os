"""add exact-action approval engine

Revision ID: 0008
Revises: 0006
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0008"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dialect = op.get_context().dialect.name

    # Enrich the approvals table with exact-action binding and lifecycle fields
    # required by APR-001 / AUT-001.
    new_approval_columns = [
        sa.Column("workspace_id", sa.Uuid(), nullable=True),
        sa.Column("run_id", sa.Uuid(), nullable=True),
        sa.Column("task_id", sa.Uuid(), nullable=True),
        sa.Column("attempt_id", sa.Uuid(), nullable=True),
        sa.Column("action_class", sa.String(length=64), nullable=True),
        sa.Column("capability_code", sa.String(length=128), nullable=True),
        sa.Column("risk_class", sa.String(length=32), nullable=True),
        sa.Column("normalized_target", sa.String(length=512), nullable=True),
        sa.Column("action_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("request_hash", sa.String(length=64), nullable=True),
        sa.Column("expected_effects", sa.Text(), nullable=True),
        sa.Column("reversibility_state", sa.String(length=32), nullable=True),
        sa.Column("data_classification", sa.String(length=32), nullable=True),
        sa.Column("policy_version", sa.String(length=64), nullable=True),
        sa.Column("required_authority", sa.String(length=128), nullable=True),
        sa.Column("independence_level", sa.String(length=32), nullable=True),
        sa.Column("requester_identity_id", sa.Uuid(), nullable=True),
        sa.Column("requester_identity_type", sa.String(length=32), nullable=True),
        sa.Column("decided_by", sa.Uuid(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    ]

    if dialect == "sqlite":
        with op.batch_alter_table("approvals") as batch_op:
            for col in new_approval_columns:
                batch_op.add_column(col)
            batch_op.create_index("ix_approvals_workspace_id", ["workspace_id"])
            batch_op.create_index("ix_approvals_run_id", ["run_id"])
            batch_op.create_index("ix_approvals_task_id", ["task_id"])
            batch_op.create_index("ix_approvals_attempt_id", ["attempt_id"])
            batch_op.create_index("ix_approvals_request_hash", ["request_hash"])
            batch_op.create_foreign_key(
                "fk_approvals_workspace_id_workspaces",
                "workspaces",
                ["workspace_id"],
                ["id"],
            )
            batch_op.create_foreign_key(
                "fk_approvals_run_id_execution_runs",
                "execution_runs",
                ["run_id"],
                ["id"],
            )
            batch_op.create_foreign_key(
                "fk_approvals_task_id_tasks", "tasks", ["task_id"], ["id"]
            )
            batch_op.create_foreign_key(
                "fk_approvals_attempt_id_run_attempts",
                "run_attempts",
                ["attempt_id"],
                ["id"],
            )
    else:
        for col in new_approval_columns:
            op.add_column("approvals", col)
        op.create_index("ix_approvals_workspace_id", "approvals", ["workspace_id"])
        op.create_index("ix_approvals_run_id", "approvals", ["run_id"])
        op.create_index("ix_approvals_task_id", "approvals", ["task_id"])
        op.create_index("ix_approvals_attempt_id", "approvals", ["attempt_id"])
        op.create_index("ix_approvals_request_hash", "approvals", ["request_hash"])
        op.create_foreign_key(
            "fk_approvals_workspace_id_workspaces",
            "approvals",
            "workspaces",
            ["workspace_id"],
            ["id"],
        )
        op.create_foreign_key(
            "fk_approvals_run_id_execution_runs",
            "approvals",
            "execution_runs",
            ["run_id"],
            ["id"],
        )
        op.create_foreign_key(
            "fk_approvals_task_id_tasks", "approvals", "tasks", ["task_id"], ["id"]
        )
        op.create_foreign_key(
            "fk_approvals_attempt_id_run_attempts",
            "approvals",
            "run_attempts",
            ["attempt_id"],
            ["id"],
        )

    # One-time atomic consumption ledger for exact-action approvals.
    op.create_table(
        "approval_consumptions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("approval_request_id", sa.Uuid(), nullable=False),
        sa.Column("approval_decision_id", sa.Uuid(), nullable=True),
        sa.Column("run_id", sa.Uuid(), nullable=False),
        sa.Column("step_id", sa.Uuid(), nullable=True),
        sa.Column("attempt_id", sa.Uuid(), nullable=False),
        sa.Column("action_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("request_version", sa.Integer(), nullable=False),
        sa.Column("policy_version", sa.String(length=64), nullable=False),
        sa.Column("consumed_by_component", sa.String(length=128), nullable=False),
        sa.Column("consumed_at", sa.DateTime(), nullable=False),
        sa.Column("execution_dispatch_reference", sa.String(length=256), nullable=True),
        sa.Column("result_reference", sa.String(length=256), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "approval_request_id", name="uq_approval_consumptions_request"
        ),
        sa.ForeignKeyConstraint(
            ["approval_request_id"], ["approvals.id"]
        ),
        sa.ForeignKeyConstraint(
            ["run_id"], ["execution_runs.id"]
        ),
        sa.ForeignKeyConstraint(
            ["attempt_id"], ["run_attempts.id"]
        ),
    )
    op.create_index(
        "ix_approval_consumptions_approval_request_id",
        "approval_consumptions",
        ["approval_request_id"],
        unique=True,
    )
    op.create_index(
        "ix_approval_consumptions_run_id", "approval_consumptions", ["run_id"]
    )
    op.create_index(
        "ix_approval_consumptions_attempt_id",
        "approval_consumptions",
        ["attempt_id"],
    )


def downgrade() -> None:
    dialect = op.get_context().dialect.name

    op.drop_index("ix_approval_consumptions_attempt_id", table_name="approval_consumptions")
    op.drop_index("ix_approval_consumptions_run_id", table_name="approval_consumptions")
    op.drop_index(
        "ix_approval_consumptions_approval_request_id",
        table_name="approval_consumptions",
    )
    op.drop_table("approval_consumptions")

    if dialect == "sqlite":
        with op.batch_alter_table("approvals") as batch_op:
            batch_op.drop_constraint(
                "fk_approvals_attempt_id_run_attempts", type_="foreignkey"
            )
            batch_op.drop_constraint("fk_approvals_task_id_tasks", type_="foreignkey")
            batch_op.drop_constraint(
                "fk_approvals_run_id_execution_runs", type_="foreignkey"
            )
            batch_op.drop_constraint(
                "fk_approvals_workspace_id_workspaces", type_="foreignkey"
            )
            batch_op.drop_index("ix_approvals_request_hash")
            batch_op.drop_index("ix_approvals_attempt_id")
            batch_op.drop_index("ix_approvals_task_id")
            batch_op.drop_index("ix_approvals_run_id")
            batch_op.drop_index("ix_approvals_workspace_id")
            batch_op.drop_column("updated_at")
            batch_op.drop_column("version")
            batch_op.drop_column("expires_at")
            batch_op.drop_column("decided_by")
            batch_op.drop_column("requester_identity_type")
            batch_op.drop_column("requester_identity_id")
            batch_op.drop_column("independence_level")
            batch_op.drop_column("required_authority")
            batch_op.drop_column("policy_version")
            batch_op.drop_column("data_classification")
            batch_op.drop_column("reversibility_state")
            batch_op.drop_column("expected_effects")
            batch_op.drop_column("request_hash")
            batch_op.drop_column("action_fingerprint")
            batch_op.drop_column("normalized_target")
            batch_op.drop_column("risk_class")
            batch_op.drop_column("capability_code")
            batch_op.drop_column("action_class")
            batch_op.drop_column("attempt_id")
            batch_op.drop_column("task_id")
            batch_op.drop_column("run_id")
            batch_op.drop_column("workspace_id")
    else:
        op.drop_constraint(
            "fk_approvals_attempt_id_run_attempts", "approvals", type_="foreignkey"
        )
        op.drop_constraint("fk_approvals_task_id_tasks", "approvals", type_="foreignkey")
        op.drop_constraint(
            "fk_approvals_run_id_execution_runs", "approvals", type_="foreignkey"
        )
        op.drop_constraint(
            "fk_approvals_workspace_id_workspaces", "approvals", type_="foreignkey"
        )
        op.drop_index("ix_approvals_request_hash", table_name="approvals")
        op.drop_index("ix_approvals_attempt_id", table_name="approvals")
        op.drop_index("ix_approvals_task_id", table_name="approvals")
        op.drop_index("ix_approvals_run_id", table_name="approvals")
        op.drop_index("ix_approvals_workspace_id", table_name="approvals")
        op.drop_column("approvals", "updated_at")
        op.drop_column("approvals", "version")
        op.drop_column("approvals", "expires_at")
        op.drop_column("approvals", "decided_by")
        op.drop_column("approvals", "requester_identity_type")
        op.drop_column("approvals", "requester_identity_id")
        op.drop_column("approvals", "independence_level")
        op.drop_column("approvals", "required_authority")
        op.drop_column("approvals", "policy_version")
        op.drop_column("approvals", "data_classification")
        op.drop_column("approvals", "reversibility_state")
        op.drop_column("approvals", "expected_effects")
        op.drop_column("approvals", "request_hash")
        op.drop_column("approvals", "action_fingerprint")
        op.drop_column("approvals", "normalized_target")
        op.drop_column("approvals", "risk_class")
        op.drop_column("approvals", "capability_code")
        op.drop_column("approvals", "action_class")
        op.drop_column("approvals", "attempt_id")
        op.drop_column("approvals", "task_id")
        op.drop_column("approvals", "run_id")
        op.drop_column("approvals", "workspace_id")
