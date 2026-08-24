"""scope execution run idempotency to task

Revision ID: 0007
Revises: 0006
"""

from alembic import op

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    dialect = op.get_context().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("execution_runs") as batch_op:
            batch_op.drop_constraint(
                "uq_execution_runs_workspace_idempotency",
                type_="unique",
            )
            batch_op.create_unique_constraint(
                "uq_execution_runs_workspace_task_idempotency",
                ["workspace_id", "task_id", "idempotency_key"],
            )
    else:
        op.drop_constraint(
            "uq_execution_runs_workspace_idempotency",
            "execution_runs",
            type_="unique",
        )
        op.create_unique_constraint(
            "uq_execution_runs_workspace_task_idempotency",
            "execution_runs",
            ["workspace_id", "task_id", "idempotency_key"],
        )


def downgrade():
    dialect = op.get_context().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("execution_runs") as batch_op:
            batch_op.drop_constraint(
                "uq_execution_runs_workspace_task_idempotency",
                type_="unique",
            )
            batch_op.create_unique_constraint(
                "uq_execution_runs_workspace_idempotency",
                ["workspace_id", "idempotency_key"],
            )
    else:
        op.drop_constraint(
            "uq_execution_runs_workspace_task_idempotency",
            "execution_runs",
            type_="unique",
        )
        op.create_unique_constraint(
            "uq_execution_runs_workspace_idempotency",
            "execution_runs",
            ["workspace_id", "idempotency_key"],
        )
