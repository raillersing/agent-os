"""Determinism test for the D0 Temporal workflow definition."""

import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from app.temporal.workflows import D0TemporalSmokeWorkflow, SmokeInput


@pytest.mark.asyncio
async def test_d0_smoke_workflow_executes_deterministically():
    async with await WorkflowEnvironment.start_time_skipping() as environment:
        client = environment.client
        async with Worker(
            client, task_queue="d0-test", workflows=[D0TemporalSmokeWorkflow]
        ):
            result = await client.execute_workflow(
                D0TemporalSmokeWorkflow.run,
                SmokeInput(run_id="smoke-1", payload="fixture"),
                id="d0-smoke-1",
                task_queue="d0-test",
            )
    assert result == {
        "run_id": "smoke-1",
        "status": "completed",
        "workflow": "d0-temporal-smoke",
        "payload": "fixture",
    }
