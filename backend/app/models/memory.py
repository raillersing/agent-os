"""
Memory Model
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Integer, Text, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..core.database import Base


class Memory(Base):
    """Memory model for storing agent knowledge."""

    __tablename__ = "memory"

    key = Column(String(255), primary_key=True)
    content = Column(Text, nullable=False)
    type = Column(String(50), default="knowledge", index=True)
    source = Column(String(255), nullable=True)
    agent_id = Column(UUID(as_uuid=True), nullable=True, index=True)

    # Metadata
    metadata_ = Column("metadata", JSON, default=dict)
    embedding_id = Column(String(255), nullable=True)  # ChromaDB reference

    # Access stats
    access_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Memory {self.key}>"
