"""Agent OS Temporal worker entrypoint for local D0 execution."""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from ..config import settings
from .activities import execute_d1_simulator_run, finalize_d1_failed_run
from .reconciliation import reconcile_pending_runs
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

        async def reconcile_loop() -> None:
            while True:
                try:
                    await reconcile_pending_runs(client)
                except Exception:
                    # A transient database or Temporal outage is retried on
                    # the next tick; committed runs remain durable meanwhile.
                    pass
                await asyncio.sleep(1)

        task = asyncio.create_task(reconcile_loop())
        try:
            await asyncio.Event().wait()
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(run_worker())
