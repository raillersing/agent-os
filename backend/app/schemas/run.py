"""
Run Schemas
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class RunOptions(BaseModel):
    """Run options."""

    stream: bool = False
    timeout: int = 30


class RunCreate(BaseModel):
    """Schema for creating a run."""

    prompt: str
    context: Optional[Dict[str, Any]] = None
    options: Optional[RunOptions] = None


class RunResult(BaseModel):
    """Run result."""

    response: Optional[str] = None
    tokens_used: Optional[int] = None
    cost: Optional[float] = None


class Run(BaseModel):
    """Full run schema."""

    id: str
    agent_id: str
    status: str
    prompt: str
    context: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
    result: Optional[RunResult] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
