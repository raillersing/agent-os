"""D1 durable simulator acceptance tests without a real provider or tool."""

import asyncio
from concurrent.futures import CancelledError as FutureCancelledError
from concurrent.futures import ThreadPoolExecutor
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, select

from app.api import control_plane
from app.core import database
from app.main import app
from app.models.control_plane import AuditEvent, ExecutionRun, RunAttempt, TaskSnapshot
from app.temporal.activities import execute_d1_simulator_run, finalize_d1_failed_run
from app.temporal.reconciliation import reconcile_pending_runs
from app.temporal.workflows import D1SimulatorRunInput

from .conftest import auth_headers


class _TemporalClient:
    async def start_workflow(self, *args, **kwargs):
        return None


class _RecordingTemporalClient(_TemporalClient):
    def __init__(self):
        self.calls = []

    async def start_workflow(self, *args, **kwargs):
        self.calls.append(kwargs["id"])


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


def test_accepted_run_is_reconciled_after_dispatch_crash(monkeypatch):
    async def crashed_connect(*args, **kwargs):
        class CrashAfterCommit:
            async def start_workflow(self, *args, **kwargs):
                raise asyncio.CancelledError("crash before dispatch acknowledgement")

        return CrashAfterCommit()

    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        monkeypatch.setattr(control_plane.Client, "connect", crashed_connect)
        with pytest.raises((asyncio.CancelledError, FutureCancelledError)):
            client.post(
                f"/api/v1/tasks/{task['id']}/runs",
                json={
                    "workspace_id": workspace["id"],
                    "input_text": "crash window",
                    "simulator_profile": "success",
                    "idempotency_key": "crash-window",
                },
            )
        runs = client.get(
            "/api/v1/execution-runs", params={"workspace_id": workspace["id"]}
        ).json()
        accepted = next(run for run in runs if run["state"] == "accepted")

    reconciler = _RecordingTemporalClient()
    assert asyncio.run(reconcile_pending_runs(reconciler)) == 1
    assert reconciler.calls == [accepted["workflow_id"]]
    assert asyncio.run(reconcile_pending_runs(reconciler)) == 0

    async def audit_dispatch_count():
        async with database.AsyncSessionLocal() as db:
            return len(
                (
                    await db.execute(
                        select(AuditEvent).where(
                            AuditEvent.resource_id == UUID(accepted["id"]),
                            AuditEvent.event_type == "run.dispatched",
                        )
                    )
                )
                .scalars()
                .all()
            )

    assert asyncio.run(audit_dispatch_count()) == 1


def test_activity_redelivery_after_terminal_success_is_idempotent(monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        payload = {
            "workspace_id": workspace["id"],
            "input_text": "redelivered",
            "simulator_profile": "success",
            "idempotency_key": "redelivered",
        }
        accepted = client.post(f"/api/v1/tasks/{task['id']}/runs", json=payload).json()

    request = D1SimulatorRunInput(
        accepted["id"], workspace["id"], "redelivered", "success"
    )
    first = asyncio.run(execute_d1_simulator_run(request))
    second = asyncio.run(execute_d1_simulator_run(request))
    assert first["state"] == second["state"] == "completed"
    with TestClient(app) as result_client:
        result_client.headers.update(auth_headers(result_client))
        result = result_client.get(
            f"/api/v1/execution-runs/{accepted['id']}",
            params={"workspace_id": workspace["id"]},
        ).json()
    assert result["state"] == "completed"
    assert len(result["attempts"]) == 1
    assert len(result["artifacts"]) == 1
    assert result["receipt"]["terminal_state"] == "completed"
    finalized = asyncio.run(finalize_d1_failed_run(accepted["id"]))
    assert finalized["state"] == "completed"


def test_workspace_isolation_covers_project_mission_task_run_evidence_and_audit(
    monkeypatch,
):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        other = client.post("/api/v1/workspaces", json={"name": "D1 other"}).json()
        project = client.get(
            f"/api/v1/projects/{task['project_id']}",
            params={"workspace_id": other["id"]},
        )
        assert project.status_code == 404
        update = client.patch(
            f"/api/v1/projects/{task['project_id']}",
            params={"workspace_id": other["id"]},
            json={"name": "leak", "expected_version": 1},
        )
        assert update.status_code == 404
        assert (
            client.get("/api/v1/missions", params={"workspace_id": other["id"]}).json()
            == []
        )
        status = client.patch(
            f"/api/v1/missions/{task['mission_id']}/status",
            params={"workspace_id": other["id"], "status": "completed"},
        )
        assert status.status_code == 404
        assert (
            client.get("/api/v1/tasks", params={"workspace_id": other["id"]}).json()
            == []
        )
        cross_task = client.post(
            "/api/v1/tasks",
            json={
                "workspace_id": other["id"],
                "project_id": task["project_id"],
                "mission_id": task["mission_id"],
                "title": "cross workspace task",
                "desired_outcome": "must fail",
            },
        )
        assert cross_task.status_code == 404
        run = client.post(
            f"/api/v1/tasks/{task['id']}/runs",
            json={
                "workspace_id": workspace["id"],
                "input_text": "isolated",
                "simulator_profile": "success",
                "idempotency_key": "isolated",
            },
        ).json()
        cross_run = client.post(
            f"/api/v1/tasks/{task['id']}/runs",
            json={
                "workspace_id": other["id"],
                "input_text": "cross workspace run",
                "simulator_profile": "success",
                "idempotency_key": "cross-workspace-run",
            },
        )
        assert cross_run.status_code == 404
        asyncio.run(
            execute_d1_simulator_run(
                D1SimulatorRunInput(run["id"], workspace["id"], "isolated", "success")
            )
        )
        assert (
            client.get(
                f"/api/v1/execution-runs/{run['id']}",
                params={"workspace_id": workspace["id"]},
            ).json()["receipt"]["terminal_state"]
            == "completed"
        )
        assert (
            client.get(
                f"/api/v1/execution-runs/{run['id']}",
                params={"workspace_id": other["id"]},
            ).status_code
            == 404
        )
        other_events = client.get(
            "/api/v1/audit-events", params={"workspace_id": other["id"]}
        ).json()
        assert all(event["workspace_id"] == other["id"] for event in other_events)
        assert all(
            event["resource_id"] not in {task["id"], run["id"]}
            for event in other_events
        )


def test_concurrent_duplicate_acceptance_returns_one_run(monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as setup_client:
        setup_client.headers.update(auth_headers(setup_client))
        workspace, task = _hierarchy(setup_client)

    payload = {
        "workspace_id": workspace["id"],
        "input_text": "concurrent",
        "simulator_profile": "success",
        "idempotency_key": "concurrent-key",
    }

    def accept_once(_):
        with TestClient(app) as concurrent_client:
            concurrent_client.headers.update(auth_headers(concurrent_client))
            response = concurrent_client.post(
                f"/api/v1/tasks/{task['id']}/runs", json=payload
            )
            return response.status_code, response.json()

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(accept_once, range(2)))
    assert all(status == 202 for status, _ in responses)
    assert {body["id"] for _, body in responses}.__len__() == 1
    assert {body["workflow_id"] for _, body in responses}.__len__() == 1

    async def persisted_counts():
        async with database.AsyncSessionLocal() as db:
            run_id = UUID(responses[0][1]["id"])
            runs = (
                (
                    await db.execute(
                        select(ExecutionRun).where(ExecutionRun.id == run_id)
                    )
                )
                .scalars()
                .all()
            )
            snapshots = (
                (
                    await db.execute(
                        select(TaskSnapshot).where(
                            TaskSnapshot.task_id == UUID(task["id"])
                        )
                    )
                )
                .scalars()
                .all()
            )
            dispatches = (
                (
                    await db.execute(
                        select(AuditEvent).where(
                            AuditEvent.resource_id == run_id,
                            AuditEvent.event_type == "run.dispatched",
                        )
                    )
                )
                .scalars()
                .all()
            )
            return len(runs), len(snapshots), len(dispatches)

    assert asyncio.run(persisted_counts()) == (1, 1, 1)


def test_concurrent_duplicate_acceptance_with_conflicting_payload_fails_closed(
    monkeypatch,
):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as setup_client:
        setup_client.headers.update(auth_headers(setup_client))
        workspace, task = _hierarchy(setup_client)

    payloads = [
        {
            "workspace_id": workspace["id"],
            "input_text": "winner A",
            "simulator_profile": "success",
            "idempotency_key": "conflicting-concurrent-key",
        },
        {
            "workspace_id": workspace["id"],
            "input_text": "winner B",
            "simulator_profile": "success",
            "idempotency_key": "conflicting-concurrent-key",
        },
    ]

    def accept(payload):
        with TestClient(app) as concurrent_client:
            concurrent_client.headers.update(auth_headers(concurrent_client))
            response = concurrent_client.post(
                f"/api/v1/tasks/{task['id']}/runs", json=payload
            )
            return response.status_code, response.json()

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(accept, payloads))
    assert {status for status, _ in responses} == {202, 409}
    assert all(status != 500 for status, _ in responses)


def test_run_attempt_unique_constraint_matches_metadata_and_migration():
    model_constraint = next(
        constraint
        for constraint in RunAttempt.__table__.constraints
        if constraint.name == "uq_run_attempts_number"
    )
    assert {column.name for column in model_constraint.columns} == {
        "run_id",
        "attempt_number",
    }

    async def database_constraint():
        async with database.engine.connect() as connection:
            return await connection.run_sync(
                lambda sync_connection: inspect(sync_connection).get_unique_constraints(
                    "run_attempts"
                )
            )

    constraints = asyncio.run(database_constraint())
    assert any(
        constraint["name"] == "uq_run_attempts_number"
        and constraint["column_names"] == ["run_id", "attempt_number"]
        for constraint in constraints
    )


def test_cancellation_completion_race_preserves_completed_evidence(monkeypatch):
    monkeypatch.setattr(control_plane.Client, "connect", _connect)
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace, task = _hierarchy(client)
        run = client.post(
            f"/api/v1/tasks/{task['id']}/runs",
            json={
                "workspace_id": workspace["id"],
                "input_text": "finish before cancel confirms",
                "simulator_profile": "success",
                "idempotency_key": "cancel-race",
            },
        ).json()

        class CompletingHandle:
            async def cancel(self):
                return None

            async def result(self):
                return await execute_d1_simulator_run(
                    D1SimulatorRunInput(
                        run["id"],
                        workspace["id"],
                        "finish before cancel confirms",
                        "success",
                    )
                )

        class CompletingClient:
            def get_workflow_handle(self, workflow_id):
                return CompletingHandle()

        async def connect_completing(*args, **kwargs):
            return CompletingClient()

        monkeypatch.setattr(control_plane.Client, "connect", connect_completing)
        response = client.post(
            f"/api/v1/execution-runs/{run['id']}/cancel",
            params={"workspace_id": workspace["id"]},
        )
        assert response.status_code == 200
        assert response.json()["state"] == "completed"
        assert response.json()["receipt"]["terminal_state"] == "completed"
