"""Temporal activity that relays pending outbox events.

This is invoked by the worker reconciliation loop. It is intentionally
idempotent: a failed dispatch can be retried safely because consumers must be
deduplicated via the inbox or by their own idempotency keys.
"""

from sqlalchemy import select

from ..core.database import AsyncSessionLocal
from ..core.time import utcnow
from ..models.outbox import OutboxEvent


async def relay_pending_outbox_events(batch_size: int = 100) -> int:
    """Dispatch pending outbox events and mark them processed.

    Returns the number of events processed.
    """
    async with AsyncSessionLocal() as db:
        events = (
            (
                await db.execute(
                    select(OutboxEvent)
                    .where(OutboxEvent.processed_at.is_(None))
                    .order_by(OutboxEvent.priority.desc(), OutboxEvent.created_at)
                    .limit(batch_size)
                )
            )
            .scalars()
            .all()
        )
        for event in events:
            try:
                # TODO: replace with real dispatch to message bus / webhooks.
                event.processed_at = utcnow()
            except Exception as error:
                event.retry_count += 1
                event.error = str(error)
        await db.commit()
    return len(events)
