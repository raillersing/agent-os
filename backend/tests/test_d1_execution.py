"""D1 durable simulator acceptance tests without a real provider or tool."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import control_plane
from app.core import database
from app.main import app

from .conftest import auth_headers


class _TemporalClient:
    async def start_workflow(self, *args, **kwargs):
        return None


async def _connect(*args, **kwargs):
    return _TemporalClient()


def _hierarchy(client: TestClient):
    suffix = uuid4().hex[:8]
    workspace = client.post("/api/v1/workspaces", json={"name": f"D1 {suffix}"}).json()
    project = client.post(
        "/api/v1/projects",
        json={
            "workspace_id": workspace["id"],
            "name": "Project",
            "purpose": "D1 proof",
        },
    ).json()
    mission = client.post(
        "/api/v1/missions",
        json={
            "workspace_id": workspace["id"],
            "project_id": project["project_id"],
            "title": "Mission",
            "objective": "Run simulator",
        },
    ).json()
    task = client.post(
        "/api/v1/tasks",
        json={
            "workspace_id": workspace["id"],
            "project_id": project["project_id"],
            "mission_id": mission["id"],
            "title": "Task",
            "desired_outcome": "Durable evidence",
        },
    ).json()
    return workspace, task


def test_d1_run_acceptance_is_idempotent_and_workspace_scoped(monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        payload = {
            "workspace_id": workspace["id"],
            "input_text": "deterministic input",
            "simulator_profile": "success",
            "idempotency_key": "d1-key",
        }
        accepted = client.post(f"/api/v1/tasks/{task['id']}/runs", json=payload)
        assert accepted.status_code == 202
        duplicate = client.post(f"/api/v1/tasks/{task['id']}/runs", json=payload)
        assert duplicate.status_code == 202
        assert duplicate.json()["id"] == accepted.json()["id"]
        conflict = client.post(
            f"/api/v1/tasks/{task['id']}/runs",
            json={**payload, "input_text": "different"},
        )
        assert conflict.status_code == 409
        other = client.post("/api/v1/workspaces", json={"name": "Other D1"}).json()
        hidden = client.get(
            f"/api/v1/execution-runs/{accepted.json()['id']}",
            params={"workspace_id": other["id"]},
        )
        assert hidden.status_code == 404
        events = client.get(
            "/api/v1/audit-events", params={"workspace_id": workspace["id"]}
        ).json()
        assert {event["event_type"] for event in events} >= {
            "task.created",
            "run.accepted",
            "run.dispatched",
        }


async def _postgres_unavailable():
    raise RuntimeError("postgresql unavailable before request handling")
    yield  # pragma: no cover


def test_postgres_unavailable_before_dispatch_fails_closed(monkeypatch):
    dispatches = 0

    async def forbidden_connect(*args, **kwargs):
        nonlocal dispatches
        dispatches += 1
        raise AssertionError("Temporal dispatch must not be attempted")

    monkeypatch.setattr(control_plane.Client, "connect", forbidden_connect)
    app.dependency_overrides[database.get_db] = _postgres_unavailable
    app.dependency_overrides[control_plane.get_db] = _postgres_unavailable
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            client.headers.update(auth_headers(client))
            response = client.post(
                f"/api/v1/tasks/{uuid4()}/runs",
                json={
                    "workspace_id": str(uuid4()),
                    "input_text": "must not dispatch",
                    "simulator_profile": "success",
                    "idempotency_key": "postgres-down",
                },
            )
        assert response.status_code == 500
        assert dispatches == 0
    finally:
        app.dependency_overrides.pop(database.get_db, None)
        app.dependency_overrides.pop(control_plane.get_db, None)
