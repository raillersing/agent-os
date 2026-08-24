"""Outbox/Inbox durable event delivery models.

Events are written to the outbox in the same database transaction as the business
state change. A background worker reads pending rows, dispatches them to
interested handlers, and marks them as processed. The inbox deduplicates
incoming events using (source, external_id).
"""

from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text, UniqueConstraint

from ..core.database import Base
from ..core.time import utcnow


class OutboxEvent(Base):
    """Outbox event waiting for durable dispatch."""

    __tablename__ = "outbox_events"

    id = Column(String(64), primary_key=True, default=lambda: uuid4().hex)
    topic = Column(String(128), nullable=False, index=True)
    payload = Column(JSON, nullable=False, default=dict)
    headers = Column(JSON, nullable=False, default=dict)
    priority = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    error = Column(Text, nullable=True)


class InboxEvent(Base):
    """Inbox event deduplicated by (source, external_id)."""

    __tablename__ = "inbox_events"

    id = Column(String(64), primary_key=True, default=lambda: uuid4().hex)
    source = Column(String(128), nullable=False)
    external_id = Column(String(256), nullable=False)
    topic = Column(String(128), nullable=False, index=True)
    payload = Column(JSON, nullable=False, default=dict)
    headers = Column(JSON, nullable=False, default=dict)
    received_at = Column(DateTime, default=utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_inbox_source_external_id"),
    )
