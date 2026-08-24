"""
Run Model
"""

import uuid

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
from sqlalchemy.orm import relationship

from ..core.database import Base
from ..core.time import utcnow


class Run(Base):
    """Run model for storing agent execution runs."""

    __tablename__ = "runs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    agent_id = Column(Uuid, ForeignKey("agents.id"), nullable=False, index=True)
    status = Column(String(50), default="pending", index=True)
    prompt = Column(Text, nullable=False)
    context = Column(JSON, default=dict)
    options = Column(JSON, default=dict)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)

    # Progress
    progress = Column(Integer, default=0)
    current_step = Column(String(255), nullable=True)
    steps = Column(JSON, default=list)

    # Stats
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    duration_ms = Column(Integer, nullable=True)

    # Timestamps
    started_at = Column(DateTime, default=utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    # Relationships
    agent = relationship("Agent", backref="runs")

    def __repr__(self):
        return f"<Run {self.id} ({self.status})>"
