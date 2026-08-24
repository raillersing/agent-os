"""Persistent MVP control-plane domain models."""

import uuid

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
from ..core.time import utcnow


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    status = Column(String(32), default="active", nullable=False, index=True)
    budget = Column(Float, default=0.0)
    spent = Column(Float, default=0.0, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


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
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


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
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


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
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


class TaskSnapshot(Base):
    """Immutable D1 execution input captured before a run is dispatched."""

    __tablename__ = "task_snapshots"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    task_id = Column(Uuid, ForeignKey("tasks.id"), nullable=False, index=True)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    input_text = Column(Text, nullable=False)
    simulator_profile = Column(String(64), nullable=False)
    execution_mode = Column(String(32), default="simulator", nullable=False)
    model_profile = Column(
        String(128), default="model.general.balanced", nullable=False
    )
    content_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)


class ExecutionRun(Base):
    """D1 durable run read model; Temporal is not its only source of truth."""

    __tablename__ = "execution_runs"
    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "task_id",
            "idempotency_key",
            name="uq_execution_runs_workspace_task_idempotency",
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
    created_at = Column(DateTime, default=utcnow, nullable=False)
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
    adapter_id = Column(String(128), nullable=True)
    adapter_version = Column(String(64), nullable=True)
    logical_model_profile = Column(String(128), nullable=True)
    configured_provider = Column(String(64), nullable=True)
    configured_model = Column(String(128), nullable=True)
    actual_provider = Column(String(64), nullable=True)
    actual_model = Column(String(128), nullable=True)
    actual_identity_state = Column(String(32), nullable=True)
    context_manifest_id = Column(Uuid, nullable=True)
    provider_request_id = Column(String(256), nullable=True)
    response_id = Column(String(256), nullable=True)
    usage_source = Column(String(32), nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    cached_input_tokens = Column(Integer, nullable=True)
    cost_state = Column(String(32), nullable=True)
    cost_amount = Column(Float, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    terminal_reason = Column(String(64), nullable=True)
    started_at = Column(DateTime, default=utcnow, nullable=False)
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
    created_at = Column(DateTime, default=utcnow, nullable=False)


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
    provider_identity = Column(String(128), nullable=True)
    input_hash = Column(String(64), nullable=False)
    output_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)


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
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


class Approval(Base):
    """Exact-action human approval request with one-time consumption binding.

    Aligns with APR-001: the request is immutable, the fingerprint binds to the
    normalized action, and consumption is recorded in a separate table so the
    consumed state survives retries, restores, and concurrent attempts.
    """

    __tablename__ = "approvals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    mission_id = Column(Uuid, ForeignKey("missions.id"), nullable=False, index=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=True, index=True)
    task_id = Column(Uuid, ForeignKey("tasks.id"), nullable=True, index=True)
    attempt_id = Column(Uuid, ForeignKey("run_attempts.id"), nullable=True, index=True)

    # Human-readable summary retained for UX and backwards compatibility.
    action = Column(String(255), nullable=False)
    scope = Column(JSON, default=dict)

    # Exact-action taxonomy and fingerprint (APR-001 §7, §12).
    action_class = Column(String(64), default="external_effect", nullable=False)
    capability_code = Column(String(128), default="manual", nullable=False)
    risk_class = Column(String(32), default="r3", nullable=False)
    normalized_target = Column(String(512), default="", nullable=False)
    action_fingerprint = Column(String(64), nullable=False)
    request_hash = Column(String(64), nullable=False, index=True)

    # Review material and policy context.
    expected_effects = Column(Text, default="", nullable=False)
    reversibility_state = Column(String(32), default="unknown", nullable=False)
    data_classification = Column(String(32), default="internal", nullable=False)
    policy_version = Column(String(64), default="AUT-001:0.2.0", nullable=False)
    required_authority = Column(String(128), default="workspace_owner", nullable=False)
    independence_level = Column(
        String(32), default="i1_requester_may_approve", nullable=False
    )

    # Identity and lifecycle.
    requester_identity_id = Column(Uuid, nullable=True)
    requester_identity_type = Column(String(32), default="human", nullable=False)
    decided_by = Column(Uuid, nullable=True)
    status = Column(String(32), default="requested", nullable=False, index=True)
    decision_note = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    decided_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)


class ApprovalConsumption(Base):
    """One-time, atomic consumption of an approved exact action.

    A separate table lets the consumed state remain append-only and unique per
    approval request, satisfying APR-INV-007 and APR-INV-008.
    """

    __tablename__ = "approval_consumptions"
    __table_args__ = (
        UniqueConstraint(
            "approval_request_id", name="uq_approval_consumptions_request"
        ),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    approval_request_id = Column(
        Uuid, ForeignKey("approvals.id"), nullable=False, unique=True, index=True
    )
    approval_decision_id = Column(Uuid, nullable=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, index=True)
    step_id = Column(Uuid, nullable=True)
    attempt_id = Column(Uuid, ForeignKey("run_attempts.id"), nullable=False, index=True)
    action_fingerprint = Column(String(64), nullable=False)
    request_version = Column(Integer, nullable=False)
    policy_version = Column(String(64), nullable=False)
    consumed_by_component = Column(String(128), nullable=False)
    consumed_at = Column(DateTime, default=utcnow, nullable=False)
    execution_dispatch_reference = Column(String(256), nullable=True)
    result_reference = Column(String(256), nullable=True)
    version = Column(Integer, default=1, nullable=False)


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
    created_at = Column(DateTime, default=utcnow, nullable=False, index=True)


class ContextManifest(Base):
    """Hash-addressed, workspace-scoped context evidence without raw secrets."""

    __tablename__ = "context_manifests"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, index=True)
    attempt_id = Column(Uuid, ForeignKey("run_attempts.id"), nullable=True, index=True)
    context_profile_id = Column(String(128), nullable=False)
    context_profile_version = Column(String(64), nullable=False)
    segments = Column(JSON, nullable=False)
    system_instruction_hash = Column(String(64), nullable=False)
    rendered_input_hash = Column(String(64), nullable=False)
    manifest_hash = Column(String(64), nullable=False, index=True)
    disclosure_state = Column(String(64), nullable=False)
    token_budget = Column(JSON, nullable=False)
    transformations = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)


class ModelInvocation(Base):
    """Provider-neutral invocation observation linked to one material attempt."""

    __tablename__ = "model_invocations"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, index=True)
    attempt_id = Column(
        Uuid, ForeignKey("run_attempts.id"), nullable=False, unique=True
    )
    context_manifest_id = Column(
        Uuid, ForeignKey("context_manifests.id"), nullable=False
    )
    adapter_id = Column(String(128), nullable=False)
    adapter_version = Column(String(64), nullable=False)
    logical_model_profile = Column(String(128), nullable=False)
    configured_provider = Column(String(64), nullable=False)
    configured_model = Column(String(128), nullable=False)
    actual_provider = Column(String(64), nullable=True)
    actual_model = Column(String(128), nullable=True)
    identity_state = Column(String(32), nullable=False)
    provider_request_id = Column(String(256), nullable=True)
    response_id = Column(String(256), nullable=True)
    prompt_hash = Column(String(64), nullable=False)
    runtime_version = Column(String(64), nullable=False)
    workflow_version = Column(String(64), nullable=False)
    policy_version = Column(String(64), nullable=False)
    invocation_state = Column(String(32), nullable=False, default="prepared")
    error_code = Column(String(96), nullable=True)
    stop_reason = Column(String(64), nullable=False)
    refusal_state = Column(String(32), nullable=False)
    tools_enabled = Column(Integer, nullable=False, default=0)
    latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)


class UsageRecord(Base):
    """Source-labelled usage and cost facts; unknown values remain NULL."""

    __tablename__ = "usage_records"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(Uuid, ForeignKey("workspaces.id"), nullable=False, index=True)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=False, index=True)
    attempt_id = Column(
        Uuid, ForeignKey("run_attempts.id"), nullable=False, unique=True
    )
    source = Column(String(32), nullable=False)
    completeness = Column(String(32), nullable=False)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    cached_input_tokens = Column(Integer, nullable=True)
    raw_usage = Column(JSON, nullable=False)
    pricing_profile_version = Column(String(64), nullable=False)
    currency = Column(String(8), nullable=False)
    cost_state = Column(String(32), nullable=False)
    estimated_cost = Column(Float, nullable=True)
    measured_cost = Column(Float, nullable=True)
    provider_reported_cost = Column(Float, nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)


class EvaluationCaseResult(Base):
    """Durable result of a bounded D2 golden evaluation case."""

    __tablename__ = "evaluation_case_results"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    suite_id = Column(String(128), nullable=False, index=True)
    suite_version = Column(String(64), nullable=False)
    case_id = Column(String(128), nullable=False)
    run_id = Column(Uuid, ForeignKey("execution_runs.id"), nullable=True, index=True)
    provider = Column(String(64), nullable=False)
    model = Column(String(128), nullable=False)
    outcome = Column(String(32), nullable=False)
    dimensions = Column(JSON, nullable=False)
    threshold_snapshot = Column(JSON, nullable=False)
    evidence_reference = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)
