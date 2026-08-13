"""Agent OS Temporal worker entrypoint for local D0 execution."""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from ..config import settings
from .workflows import D0TemporalSmokeWorkflow


async def run_worker() -> None:
    client = await Client.connect(
        settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE
    )
    async with Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[D0TemporalSmokeWorkflow],
    ):
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(run_worker())
