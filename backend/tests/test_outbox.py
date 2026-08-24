"""Outbox and inbox tests."""

from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.outbox import InboxEvent, OutboxEvent
from app.services.outbox import record_inbox_event, schedule_outbox_event


@pytest.mark.asyncio
async def test_schedule_and_process_outbox_event():
    async with AsyncSessionLocal() as db:
        event = await schedule_outbox_event(
            db,
            topic="run.completed",
            payload={"run_id": str(uuid4())},
            headers={"source": "test"},
            priority=1,
        )
        await db.commit()
        assert event.id
        assert event.topic == "run.completed"
        assert event.processed_at is None

        pending = (
            (
                await db.execute(
                    select(OutboxEvent).where(OutboxEvent.processed_at.is_(None))
                )
            )
            .scalars()
            .all()
        )
        assert any(e.id == event.id for e in pending)


@pytest.mark.asyncio
async def test_inbox_deduplicates_by_source_and_external_id():
    async with AsyncSessionLocal() as db:
        first = await record_inbox_event(
            db,
            source="webhook",
            external_id="evt-123",
            topic="external.run.completed",
            payload={"ok": True},
        )
        assert first is not None
        duplicate = await record_inbox_event(
            db,
            source="webhook",
            external_id="evt-123",
            topic="external.run.completed",
            payload={"ok": True},
        )
        assert duplicate is None
        await db.commit()

        rows = (
            (
                await db.execute(
                    select(InboxEvent).where(
                        InboxEvent.source == "webhook",
                        InboxEvent.external_id == "evt-123",
                    )
                )
            )
            .scalars()
            .all()
        )
        assert len(rows) == 1


@pytest.mark.asyncio
async def test_inbox_allows_same_external_id_from_different_sources():
    async with AsyncSessionLocal() as db:
        a = await record_inbox_event(
            db,
            source="webhook-a",
            external_id="evt-456",
            topic="t",
            payload={},
        )
        b = await record_inbox_event(
            db,
            source="webhook-b",
            external_id="evt-456",
            topic="t",
            payload={},
        )
        assert a is not None
        assert b is not None
        await db.commit()
