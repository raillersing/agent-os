"""Pydantic contracts for the persistent control plane."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ORMModel(BaseModel):
    class Config:
        from_attributes = True


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = ""
    budget: float = Field(default=0, ge=0)


class Workspace(WorkspaceCreate, ORMModel):
    id: UUID
    status: str
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
    workspace_id: UUID
    input_text: str = Field(min_length=1)
    simulator_profile: str = Field(
        default="success",
        pattern="^(success|retryable_failure|non_retryable_failure|timeout|unknown_cost|slow_success)$",
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
    started_at: datetime
    ended_at: datetime | None


class Artifact(ORMModel):
    id: UUID
    media_type: str
    content_hash: str
    state: str
    created_at: datetime


class ExecutionReceipt(ORMModel):
    id: UUID
    terminal_state: str
    reason_code: str | None
    simulator_identity: str
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
    action: str = Field(min_length=1, max_length=255)
    scope: dict[str, Any] = {}


class ApprovalDecision(BaseModel):
    status: str = Field(pattern="^(approved|rejected)$")
    decision_note: str | None = None


class Approval(ApprovalCreate, ORMModel):
    id: UUID
    status: str
    decision_note: str | None
    created_at: datetime
    decided_at: datetime | None


class AuditEvent(ORMModel):
    id: UUID
    workspace_id: UUID
    event_type: str
    resource_type: str
    resource_id: UUID
    actor: str
    details: dict[str, Any]
    created_at: datetime
