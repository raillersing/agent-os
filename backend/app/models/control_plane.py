"""Persistent MVP control-plane domain models."""

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)

from ..core.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    status = Column(String(32), default="active", nullable=False, index=True)
    budget = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Project(Base):
    """Durable body of work inside one workspace."""

    __tablename__ = "projects"

    project_id = Column("id", Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    purpose = Column(Text, nullable=False)
    state = Column(String(32), default="active", nullable=False, index=True)
    created_by = Column(Uuid, nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    # Nullable only for rows created before D0. New API writes require a project.
    project_id = Column(Uuid, ForeignKey("projects.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    objective = Column(Text, nullable=False)
    status = Column(String(32), default="draft", nullable=False, index=True)
    progress = Column(Integer, default=0, nullable=False)
    plan = Column(JSON, default=list)
    evidence = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Task(Base):
    """Executable unit owned by a mission and its workspace project."""

    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(Uuid, ForeignKey("projects.id"), nullable=False, index=True)
    mission_id = Column(Uuid, ForeignKey("missions.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    desired_outcome = Column(Text, nullable=False)
    state = Column(String(32), default="ready", nullable=False, index=True)
    created_by = Column(Uuid, nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class TaskSnapshot(Base):
    """Immutable D1 execution input captured before a run is dispatched."""

    __tablename__ = "task_snapshots"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    task_id = Column(Uuid, ForeignKey("tasks.id"), nullable=False, index=True)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    input_text = Column(Text, nullable=False)
    simulator_profile = Column(String(64), nullable=False)
    content_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ExecutionRun(Base):
    """D1 durable run read model; Temporal is not its only source of truth."""

    __tablename__ = "execution_runs"
    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "idempotency_key",
            name="uq_execution_runs_workspace_idempotency",
        ),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(Uuid, ForeignKey("projects.id"), nullable=False, index=True)
    mission_id = Column(Uuid, ForeignKey("missions.id"), nullable=False, index=True)
    task_id = Column(Uuid, ForeignKey("tasks.id"), nullable=False, index=True)
    task_snapshot_id = Column(
        Uuid, ForeignKey("task_snapshots.id"), nullable=False, index=True
    )
    state = Column(String(32), default="accepted", nullable=False, index=True)
    state_reason = Column(String(96), nullable=True)
    idempotency_key = Column(String(128), nullable=False)
    request_hash = Column(String(64), nullable=False)
    correlation_id = Column(Uuid, nullable=False, index=True)
    workflow_id = Column(String(128), nullable=False, unique=True)
    cancellation_state = Column(String(32), default="not_requested", nullable=False)
    receipt_state = Column(String(32), default="pending", nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    last_reliable_evidence_at = Column(DateTime, nullable=True)


class RunAttempt(Base):
    """Append-only execution attribution for one simulator Activity invocation."""

    __tablename__ = "run_attempts"
    __table_args__ = (
        UniqueConstraint("run_id", "attempt_number", name="uq_run_attempts_number"),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, index=True)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    attempt_number = Column(Integer, nullable=False)
    idempotency_key = Column(String(160), nullable=False)
    state = Column(String(32), nullable=False, index=True)
    failure_kind = Column(String(64), nullable=True)
    provider_identity = Column(String(128), nullable=False)
    side_effect_certainty = Column(String(32), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)


class Artifact(Base):
    """Immutable simulator material output metadata and integrity reference."""

    __tablename__ = "artifacts"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, index=True)
    attempt_id = Column(Uuid, ForeignKey("run_attempts.id"), nullable=False, index=True)
    media_type = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    # The hash identifies immutable content; identical simulator output may
    # legitimately be produced by different Runs, so identity remains per
    # Artifact rather than globally unique by hash.
    content_hash = Column(String(64), nullable=False)
    state = Column(String(32), default="accepted", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ExecutionReceipt(Base):
    """Evidence summary for a terminal D1 simulator run."""

    __tablename__ = "execution_receipts"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, unique=True)
    attempt_id = Column(Uuid, ForeignKey("run_attempts.id"), nullable=True, index=True)
    artifact_id = Column(Uuid, ForeignKey("artifacts.id"), nullable=True, index=True)
    terminal_state = Column(String(32), nullable=False)
    reason_code = Column(String(96), nullable=True)
    simulator_identity = Column(String(128), nullable=False)
    input_hash = Column(String(64), nullable=False)
    output_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Automation(Base):
    __tablename__ = "automations"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    trigger_type = Column(String(64), nullable=False)
    trigger_config = Column(JSON, default=dict)
    steps = Column(JSON, default=list)
    enabled = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    mission_id = Column(Uuid, ForeignKey("missions.id"), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    scope = Column(JSON, default=dict)
    status = Column(String(32), default="pending", nullable=False, index=True)
    decision_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    decided_at = Column(DateTime, nullable=True)


class AuditEvent(Base):
    """Append-only operational evidence for workspace-scoped mutations."""

    __tablename__ = "audit_events"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    event_type = Column(String(96), nullable=False, index=True)
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(Uuid, nullable=False, index=True)
    actor = Column(String(128), nullable=False, default="local-system")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
