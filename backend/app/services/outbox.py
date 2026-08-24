"""Outbox/Inbox helpers for durable event delivery.

Events are written to the outbox in the same transaction as the business state
change. A separate worker dispatches pending rows; handlers that receive
external events write to the inbox for deduplication.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.outbox import InboxEvent, OutboxEvent


async def schedule_outbox_event(
    db: AsyncSession,
    *,
    topic: str,
    payload: dict,
    headers: dict | None = None,
    priority: int = 0,
) -> OutboxEvent:
    """Schedule an outbox event in the current transaction."""
    event = OutboxEvent(
        topic=topic,
        payload=payload,
        headers=headers or {},
        priority=priority,
    )
    db.add(event)
    await db.flush()
    return event


async def record_inbox_event(
    db: AsyncSession,
    *,
    source: str,
    external_id: str,
    topic: str,
    payload: dict,
    headers: dict | None = None,
) -> InboxEvent | None:
    """Record an external event in the inbox; returns None if already seen.

    Callers must commit the transaction themselves.
    """
    existing = (
        await db.execute(
            select(InboxEvent).where(
                InboxEvent.source == source, InboxEvent.external_id == external_id
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        return None
    event = InboxEvent(
        source=source,
        external_id=external_id,
        topic=topic,
        payload=payload,
        headers=headers or {},
    )
    db.add(event)
    await db.flush()
    return event
