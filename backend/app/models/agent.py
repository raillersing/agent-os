"""
Agent Model
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Uuid,
)

from ..core.database import Base


class Agent(Base):
    """Agent model for storing agent configurations."""

    __tablename__ = "agents"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    status = Column(String(50), default="active", index=True)
    description = Column(Text, nullable=True)
    capabilities = Column(JSON, default=list)
    config = Column(JSON, default=dict)
    policies = Column(JSON, default=dict)

    # Stats
    total_runs = Column(Integer, default=0)
    successful_runs = Column(Integer, default=0)
    failed_runs = Column(Integer, default=0)
    total_tokens = Column(BigInteger, default=0)
    total_cost = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_run_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Agent {self.name} ({self.model})>"
