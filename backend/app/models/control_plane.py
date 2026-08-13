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
