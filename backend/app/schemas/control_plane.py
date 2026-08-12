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


class MissionCreate(BaseModel):
    workspace_id: UUID
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
