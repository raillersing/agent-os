"""Pydantic contracts for the persistent control plane."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = ""
    budget: float = Field(default=0, ge=0)


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    budget: float | None = Field(default=None, ge=0)
    spent: float | None = None
    status: str | None = None
    expected_version: int | None = None


class Workspace(WorkspaceCreate, ORMModel):
    id: UUID
    status: str
    spent: float
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    workspace_id: UUID
    name: str = Field(min_length=1, max_length=255)
    purpose: str = Field(min_length=1)


class Project(ProjectCreate, ORMModel):
    project_id: UUID
    state: str
    created_by: UUID
    version: int
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    purpose: str | None = Field(default=None, min_length=1)
    state: str | None = Field(default=None, pattern="^(active|paused|archived)$")
    expected_version: int = Field(ge=1)


class MissionCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID
    title: str = Field(min_length=1, max_length=255)
    objective: str = Field(min_length=1)
    plan: list[dict[str, Any]] = []


class Mission(MissionCreate, ORMModel):
    id: UUID
    status: str
    progress: int
    evidence: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    workspace_id: UUID
    project_id: UUID
    mission_id: UUID
    title: str = Field(min_length=1, max_length=255)
    desired_outcome: str = Field(min_length=1)


class Task(TaskCreate, ORMModel):
    id: UUID
    state: str
    created_by: UUID
    version: int
    created_at: datetime
    updated_at: datetime


class ExecutionRunCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    workspace_id: UUID
    input_text: str = Field(min_length=1)
    simulator_profile: str = Field(
        default="success",
        pattern="^(success|retryable_failure|non_retryable_failure|timeout|unknown_cost|slow_success)$",
    )
    execution_mode: str = Field(default="simulator", pattern="^(simulator|openai)$")
    model_profile: str = Field(
        default="model.general.balanced", min_length=1, max_length=128
    )
    idempotency_key: str = Field(min_length=1, max_length=128)
    correlation_id: UUID | None = None


class RunAttempt(ORMModel):
    id: UUID
    attempt_number: int
    state: str
    failure_kind: str | None
    provider_identity: str
    side_effect_certainty: str
    adapter_id: str | None = None
    adapter_version: str | None = None
    logical_model_profile: str | None = None
    configured_provider: str | None = None
    configured_model: str | None = None
    actual_provider: str | None = None
    actual_model: str | None = None
    actual_identity_state: str | None = None
    context_manifest_id: UUID | None = None
    provider_request_id: str | None = None
    response_id: str | None = None
    usage_source: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cached_input_tokens: int | None = None
    cost_state: str | None = None
    cost_amount: float | None = None
    latency_ms: int | None = None
    terminal_reason: str | None = None
    started_at: datetime
    ended_at: datetime | None


class Artifact(ORMModel):
    id: UUID
    workspace_id: UUID
    run_id: UUID
    attempt_id: UUID
    media_type: str
    content: str
    content_hash: str
    state: str
    created_at: datetime


class ExecutionReceipt(ORMModel):
    id: UUID
    terminal_state: str
    reason_code: str | None
    simulator_identity: str
    provider_identity: str | None = None
    input_hash: str
    output_hash: str | None
    created_at: datetime


class ExecutionRun(ORMModel):
    id: UUID
    workspace_id: UUID
    project_id: UUID
    mission_id: UUID
    task_id: UUID
    task_snapshot_id: UUID
    state: str
    state_reason: str | None
    correlation_id: UUID
    workflow_id: str
    cancellation_state: str
    receipt_state: str
    version: int
    created_at: datetime
    started_at: datetime | None
    ended_at: datetime | None
    execution_mode: str = "simulator"
    model_profile: str = "model.general.balanced"
    retry_count: int = 0
    attempts: list[RunAttempt] = []
    artifacts: list[Artifact] = []
    receipt: ExecutionReceipt | None = None


class AutomationCreate(BaseModel):
    workspace_id: UUID
    name: str = Field(min_length=1, max_length=255)
    description: str = ""
    trigger_type: str = Field(min_length=1, max_length=64)
    trigger_config: dict[str, Any] = {}
    steps: list[dict[str, Any]] = []


class Automation(AutomationCreate, ORMModel):
    id: UUID
    enabled: int
    created_at: datetime
    updated_at: datetime


class ApprovalCreate(BaseModel):
    mission_id: UUID
    workspace_id: UUID | None = None
    action: str = Field(min_length=1, max_length=255)
    scope: dict[str, Any] = {}
    run_id: UUID | None = None
    task_id: UUID | None = None
    action_class: str = Field(default="external_effect", max_length=64)
    capability_code: str = Field(default="manual", max_length=128)
    risk_class: str = Field(default="r3", max_length=32)
    normalized_target: str = Field(default="", max_length=512)
    expected_effects: str = ""
    reversibility_state: str = Field(default="unknown", max_length=32)
    data_classification: str = Field(default="internal", max_length=32)
    policy_version: str = Field(default="AUT-001:0.2.0", max_length=64)
    required_authority: str = Field(default="workspace_owner", max_length=128)
    independence_level: str = Field(default="i1_requester_may_approve", max_length=32)
    expires_at: datetime | None = None


class ApprovalDecision(BaseModel):
    status: str = Field(pattern="^(approved|rejected|revision_requested|cancelled)$")
    decision_note: str | None = None


class ApprovalConsumeRequest(BaseModel):
    run_id: UUID
    attempt_id: UUID
    action_fingerprint: str = Field(min_length=1, max_length=64)
    execution_dispatch_reference: str | None = Field(default=None, max_length=256)
    consumed_by_component: str = Field(default="tool_gateway", max_length=128)


class ApprovalInvalidateRequest(BaseModel):
    reason_code: str = Field(min_length=1, max_length=64)
    evidence_reference: str | None = Field(default=None, max_length=256)


class Approval(ApprovalCreate, ORMModel):
    id: UUID
    attempt_id: UUID | None
    action_fingerprint: str
    request_hash: str
    status: str
    requester_identity_id: UUID | None
    requester_identity_type: str
    decided_by: UUID | None
    decision_note: str | None
    version: int
    created_at: datetime
    decided_at: datetime | None
    updated_at: datetime


class ApprovalConsumption(ORMModel):
    id: UUID
    approval_request_id: UUID
    run_id: UUID
    attempt_id: UUID
    action_fingerprint: str
    request_version: int
    policy_version: str
    consumed_by_component: str
    consumed_at: datetime
    execution_dispatch_reference: str | None
    result_reference: str | None
    version: int


class AuditEvent(ORMModel):
    id: UUID
    workspace_id: UUID
    event_type: str
    resource_type: str
    resource_id: UUID
    actor: str
    details: dict[str, Any]
    created_at: datetime
