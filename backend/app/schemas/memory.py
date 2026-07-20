"""
Memory Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    """Schema for creating memory."""

    key: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    ttl: Optional[int] = None


class Memory(BaseModel):
    """Full memory schema."""

    key: str
    content: str
    metadata: Dict[str, Any] = {}
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MemorySearchResults(BaseModel):
    """Memory search results."""

    results: List[Memory]
    total: int
