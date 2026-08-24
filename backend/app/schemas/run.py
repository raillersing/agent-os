"""
Run Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RunOptions(BaseModel):
    """Run options."""

    stream: bool = False
    timeout: int = 30


class RunCreate(BaseModel):
    """Schema for creating a run."""

    prompt: str
    context: Optional[Dict[str, Any]] = None
    options: Optional[RunOptions] = None


class RunStep(BaseModel):
    """Run step."""

    name: str
    status: str
    duration: Optional[str] = None


class RunResult(BaseModel):
    """Run result."""

    response: Optional[str] = None
    tokens_used: Optional[int] = None
    cost: Optional[float] = None


class Run(BaseModel):
    """Full run schema."""

    id: UUID
    agent_id: UUID
    status: str
    prompt: str
    context: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: int = 0
    current_step: Optional[str] = None
    steps: List[Dict[str, Any]] = []
    tokens_used: int = 0
    cost: float = 0.0
    duration_ms: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
