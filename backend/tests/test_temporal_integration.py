"""Temporal integration tests using an in-process local server."""

import asyncio

import pytest
from fastapi.testclient import TestClient
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from app.api import control_plane
from app.config import settings
from app.main import app
from app.temporal.activities import execute_d1_simulator_run, finalize_d1_failed_run
from app.temporal.workflows import D1SimulatorRunInput, D1SimulatorRunWorkflow

from .conftest import auth_headers
from .test_d1_execution import _connect, _hierarchy


@pytest.fixture(scope="module")
def temporal_env():
    env = asyncio.run(WorkflowEnvironment.start_local())
    yield env
    asyncio.run(env.shutdown())


async def _run_d1_workflow(
    env: WorkflowEnvironment, run_id: str, workspace_id: str
) -> dict:
    client = env.client
    async with Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[D1SimulatorRunWorkflow],
        activities=[execute_d1_simulator_run, finalize_d1_failed_run],
    ):
        return await client.execute_workflow(
            D1SimulatorRunWorkflow.run,
            D1SimulatorRunInput(
                run_id=run_id,
                workspace_id=workspace_id,
                input_text="temporal integration run",
                simulator_profile="success",
                execution_mode="simulator",
                model_profile="model.general.balanced",
            ),
            id=f"d1-integration-{run_id}",
            task_queue=settings.TEMPORAL_TASK_QUEUE,
        )


def test_d1_simulator_workflow_completes_run(temporal_env, monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        payload = {
            "workspace_id": workspace["id"],
            "input_text": "temporal integration run",
            "simulator_profile": "success",
            "idempotency_key": "temporal-integration",
        }
        run = client.post(f"/api/v1/tasks/{task['id']}/runs", json=payload).json()
        run_id = run["id"]

    result = asyncio.run(_run_d1_workflow(temporal_env, run_id, workspace["id"]))
    assert result["state"] == "completed"

    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        response = client.get(
            f"/api/v1/execution-runs/{run_id}",
            params={"workspace_id": workspace["id"]},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["state"] == "completed"
        assert body["receipt"]["terminal_state"] == "completed"
        assert len(body["artifacts"]) >= 1
