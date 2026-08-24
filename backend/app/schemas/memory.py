"""
Memory Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MemoryCreate(BaseModel):
    """Schema for creating memory."""

    key: str
    content: str
    type: Optional[str] = "knowledge"
    source: Optional[str] = None
    agent_id: Optional[UUID] = None
    metadata_: Optional[Dict[str, Any]] = None
    ttl: Optional[int] = None


class Memory(BaseModel):
    """Full memory schema."""

    key: str
    content: str
    type: str
    source: Optional[str] = None
    agent_id: Optional[UUID] = None
    metadata_: Dict[str, Any] = {}
    access_count: int = 0
    last_accessed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MemorySearchResults(BaseModel):
    """Memory search results."""

    results: List[Memory]
    total: int
