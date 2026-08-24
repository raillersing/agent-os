"""End-to-end HTTP API integration tests."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import control_plane
from app.main import app

from .conftest import auth_headers


async def _no_op_temporal_connect(*args, **kwargs):
    class _NoOpClient:
        async def start_workflow(self, *args, **kwargs):
            return None

    return _NoOpClient()


def test_full_control_plane_lifecycle(monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _no_op_temporal_connect)
    suffix = uuid4().hex[:8]
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))

        workspace = client.post(
            "/api/v1/workspaces",
            json={
                "name": f"Integration {suffix}",
                "description": "E2E test",
                "budget": 50,
            },
        ).json()
        assert workspace["name"] == f"Integration {suffix}"

        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": f"Project {suffix}",
                "purpose": "E2E test",
            },
        ).json()
        assert project["workspace_id"] == workspace["id"]

        mission = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "title": f"Mission {suffix}",
                "objective": "E2E test",
                "plan": [{"name": "Step 1", "status": "planned"}],
            },
        ).json()
        assert mission["workspace_id"] == workspace["id"]

        task = client.post(
            "/api/v1/tasks",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "mission_id": mission["id"],
                "title": f"Task {suffix}",
                "desired_outcome": "E2E test",
            },
        ).json()
        assert task["mission_id"] == mission["id"]

        run = client.post(
            f"/api/v1/tasks/{task['id']}/runs",
            json={
                "workspace_id": workspace["id"],
                "input_text": "e2e run",
                "simulator_profile": "success",
                "idempotency_key": f"e2e-{suffix}",
            },
        )
        assert run.status_code == 202
        run_body = run.json()
        assert run_body["workspace_id"] == workspace["id"]
        assert run_body["task_id"] == task["id"]

        get_run = client.get(
            f"/api/v1/execution-runs/{run_body['id']}",
            params={"workspace_id": workspace["id"]},
        )
        assert get_run.status_code == 200
        assert get_run.json()["id"] == run_body["id"]

        missions = client.get(
            "/api/v1/missions", params={"workspace_id": workspace["id"]}
        ).json()
        assert any(m["id"] == mission["id"] for m in missions)

        automations = client.post(
            "/api/v1/automations",
            json={
                "workspace_id": workspace["id"],
                "name": f"Automation {suffix}",
                "trigger_type": "manual",
                "trigger_config": {},
                "steps": [{"name": "Step 1"}],
            },
        ).json()
        assert automations["workspace_id"] == workspace["id"]

        approval = client.post(
            "/api/v1/approvals",
            params={"workspace_id": workspace["id"]},
            json={
                "mission_id": mission["id"],
                "action": "approve e2e step",
                "scope": {"mode": "test"},
            },
        ).json()
        assert approval["mission_id"] == mission["id"]
        assert approval["status"] == "pending"

        decided = client.post(
            f"/api/v1/approvals/{approval['id']}/decision",
            params={"workspace_id": workspace["id"]},
            json={"status": "approved", "decision_note": "E2E approved"},
        ).json()
        assert decided["status"] == "approved"

        audits = client.get(
            "/api/v1/audit-events",
            params={"workspace_id": workspace["id"], "limit": 50},
        ).json()
        assert len(audits) > 0
