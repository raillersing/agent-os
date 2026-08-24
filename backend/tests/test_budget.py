"""Workspace budget tests."""

import asyncio
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from temporalio.exceptions import ApplicationError

from app.api import control_plane
from app.main import app
from app.temporal.activities import execute_d1_simulator_run
from app.temporal.workflows import D1SimulatorRunInput

from .conftest import auth_headers
from .test_d1_execution import _connect, _hierarchy


def test_workspace_budget_blocks_run_when_exhausted(monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        # Set a tiny budget and exhaust it
        client.patch(
            f"/api/v1/workspaces/{workspace['id']}",
            json={"budget": 0.01, "expected_version": 1},
        )
        client.patch(
            f"/api/v1/workspaces/{workspace['id']}",
            json={"spent": 0.02, "expected_version": 2},
        )
        payload = {
            "workspace_id": workspace["id"],
            "input_text": "budget exhausted",
            "simulator_profile": "success",
            "idempotency_key": f"budget-{uuid4().hex[:8]}",
        }
        run = client.post(f"/api/v1/tasks/{task['id']}/runs", json=payload).json()

    with pytest.raises(ApplicationError, match="MODEL_BUDGET_EXHAUSTED"):
        asyncio.run(
            execute_d1_simulator_run(
                D1SimulatorRunInput(
                    run["id"],
                    workspace["id"],
                    "budget exhausted",
                    "success",
                    "simulator",
                    "model.general.balanced",
                )
            )
        )
    result = client.get(
        f"/api/v1/execution-runs/{run['id']}",
        params={"workspace_id": workspace["id"]},
    ).json()
    assert result["state"] == "failed"
    assert result["state_reason"] == "MODEL_BUDGET_EXHAUSTED"
