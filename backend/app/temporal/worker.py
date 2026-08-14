"""Agent OS Temporal worker entrypoint for local D0 execution."""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from ..config import settings
from .activities import execute_d1_simulator_run, finalize_d1_failed_run
from .workflows import D0TemporalSmokeWorkflow, D1SimulatorRunWorkflow


async def run_worker() -> None:
    client = await Client.connect(
        settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE
    )
    async with Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[D0TemporalSmokeWorkflow, D1SimulatorRunWorkflow],
        activities=[execute_d1_simulator_run, finalize_d1_failed_run],
    ):
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(run_worker())
