"""
Agent Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AgentBase(BaseModel):
    """Base agent schema."""

    name: str
    model: str
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None
    policies: Optional[Dict[str, Any]] = None


class AgentCreate(AgentBase):
    """Schema for creating an agent."""

    pass


class AgentUpdate(BaseModel):
    """Schema for updating an agent."""

    name: Optional[str] = None
    model: Optional[str] = None
    status: Optional[Literal["active", "inactive"]] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None
    policies: Optional[Dict[str, Any]] = None


class Agent(AgentBase):
    """Full agent schema."""

    id: UUID
    status: Literal["active", "inactive", "error"]
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    created_at: datetime
    updated_at: datetime
    last_run_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
