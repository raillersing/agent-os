"""add first-class projects and link new missions to them

Revision ID: 0004
Revises: 0003

Existing missions intentionally retain a nullable project_id during this
compatibility migration. New API-created missions require project_id; a later
data migration may backfill legacy rows when the product supplies a mapping.
"""

import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "projects",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "workspace_id", sa.Uuid(), sa.ForeignKey("workspaces.id"), nullable=False
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_projects_workspace_id", "projects", ["workspace_id"])
    op.create_index("ix_projects_state", "projects", ["state"])
    op.create_index("ix_projects_created_by", "projects", ["created_by"])
    op.add_column("missions", sa.Column("project_id", sa.Uuid(), nullable=True))
    op.create_index("ix_missions_project_id", "missions", ["project_id"])
    dialect = op.get_context().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("missions") as batch_op:
            batch_op.create_foreign_key(
                "fk_missions_project_id_projects",
                "projects",
                ["project_id"],
                ["id"],
            )
    else:
        op.create_foreign_key(
            "fk_missions_project_id_projects",
            "missions",
            "projects",
            ["project_id"],
            ["id"],
        )


def downgrade():
    dialect = op.get_context().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("missions") as batch_op:
            batch_op.drop_constraint(
                "fk_missions_project_id_projects", type_="foreignkey"
            )
    else:
        op.drop_constraint(
            "fk_missions_project_id_projects", "missions", type_="foreignkey"
        )
    op.drop_index("ix_missions_project_id", table_name="missions")
    op.drop_column("missions", "project_id")
    op.drop_index("ix_projects_created_by", table_name="projects")
    op.drop_index("ix_projects_state", table_name="projects")
    op.drop_index("ix_projects_workspace_id", table_name="projects")
    op.drop_table("projects")
