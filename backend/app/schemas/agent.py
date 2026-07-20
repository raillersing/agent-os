"""
Agent Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AgentBase(BaseModel):
    """Base agent schema."""

    name: str
    model: str
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
    status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    policies: Optional[Dict[str, Any]] = None


class Agent(AgentBase):
    """Full agent schema."""

    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
