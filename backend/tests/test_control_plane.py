"""Persistence and governance tests for the MVP control plane."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

from .conftest import auth_headers


def test_workspace_mission_automation_and_approval_persist_across_clients():
    suffix = uuid4().hex[:8]

    with TestClient(app) as first_client:
        first_client.headers.update(auth_headers(first_client))
        workspace_response = first_client.post(
            "/api/v1/workspaces",
            json={
                "name": f"Workspace {suffix}",
                "description": "Persistence proof",
                "budget": 100,
            },
        )
        assert workspace_response.status_code == 201
        workspace = workspace_response.json()

        project_response = first_client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": f"Project {suffix}",
                "purpose": "Persistence proof",
            },
        )
        assert project_response.status_code == 201
        project = project_response.json()
        assert project["state"] == "active"
        assert project["version"] == 1
        assert project["purpose"] == "Persistence proof"
        assert project["created_by"]

        mission_response = first_client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "title": f"Mission {suffix}",
                "objective": "Prove durable mission state",
                "plan": [{"name": "Persist", "status": "planned"}],
            },
        )
        assert mission_response.status_code == 201
        mission = mission_response.json()

        automation_response = first_client.post(
            "/api/v1/automations",
            json={
                "workspace_id": workspace["id"],
                "name": f"Automation {suffix}",
                "trigger_type": "schedule",
                "trigger_config": {"cron": "0 8 * * 1"},
                "steps": [{"name": "Prepare brief"}],
            },
        )
        assert automation_response.status_code == 201

        approval_response = first_client.post(
            "/api/v1/approvals",
            json={
                "mission_id": mission["id"],
                "action": "Read customer interviews",
                "scope": {"mode": "read", "files": 18},
            },
        )
        assert approval_response.status_code == 201
        approval = approval_response.json()

    # A new application client proves state is not held in process memory.
    with TestClient(app) as restarted_client:
        restarted_client.headers.update(auth_headers(restarted_client))
        workspaces = restarted_client.get("/api/v1/workspaces").json()
        assert any(item["id"] == workspace["id"] for item in workspaces)

        projects = restarted_client.get(
            "/api/v1/projects", params={"workspace_id": workspace["id"]}
        )
        assert projects.status_code == 200
        assert [item["project_id"] for item in projects.json()] == [
            project["project_id"]
        ]
        project_get = restarted_client.get(
            f"/api/v1/projects/{project['project_id']}",
            params={"workspace_id": workspace["id"]},
        )
        assert project_get.status_code == 200
        assert project_get.json()["workspace_id"] == workspace["id"]

        missions = restarted_client.get(
            "/api/v1/missions", params={"workspace_id": workspace["id"]}
        ).json()
        assert [item["id"] for item in missions] == [mission["id"]]

        automations = restarted_client.get(
            "/api/v1/automations", params={"workspace_id": workspace["id"]}
        ).json()
        assert len(automations) == 1

        decision = restarted_client.post(
            f"/api/v1/approvals/{approval['id']}/decision",
            json={
                "status": "approved",
                "decision_note": "Approved for this mission only",
            },
        )
        assert decision.status_code == 200
        assert decision.json()["status"] == "approved"

        duplicate = restarted_client.post(
            f"/api/v1/approvals/{approval['id']}/decision",
            json={"status": "approved"},
        )
        assert duplicate.status_code == 409

        events = restarted_client.get(
            "/api/v1/audit-events", params={"workspace_id": workspace["id"]}
        )
        assert events.status_code == 200
        event_types = {event["event_type"] for event in events.json()}
        assert {
            "workspace.created",
            "mission.created",
            "automation.created",
            "approval.requested",
            "approval.approved",
        } <= event_types


def test_mission_rejects_unknown_workspace():
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        response = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": str(uuid4()),
                "project_id": str(uuid4()),
                "title": "Invalid mission",
                "objective": "Must not cross an unknown workspace boundary",
            },
        )
        assert response.status_code == 404


def test_workspace_filters_do_not_return_another_workspace_records():
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        first = client.post(
            "/api/v1/workspaces", json={"name": f"First {uuid4().hex[:8]}"}
        ).json()
        second = client.post(
            "/api/v1/workspaces", json={"name": f"Second {uuid4().hex[:8]}"}
        ).json()
        first_project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": first["id"],
                "name": "First project",
                "purpose": "Scoped test",
            },
        ).json()
        mission = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": first["id"],
                "project_id": first_project["project_id"],
                "title": "Private mission",
                "objective": "Stay scoped",
            },
        ).json()
        automation = client.post(
            "/api/v1/automations",
            json={
                "workspace_id": first["id"],
                "name": "Private automation",
                "trigger_type": "manual",
            },
        ).json()

        assert [
            item["id"]
            for item in client.get(
                "/api/v1/missions", params={"workspace_id": second["id"]}
            ).json()
        ] == []
        assert (
            client.get("/api/v1/projects", params={"workspace_id": second["id"]}).json()
            == []
        )
        assert [
            item["id"]
            for item in client.get(
                "/api/v1/automations", params={"workspace_id": second["id"]}
            ).json()
        ] == []
        assert mission["workspace_id"] == first["id"]
        assert automation["workspace_id"] == first["id"]

        audit_events = client.get(
            "/api/v1/audit-events", params={"workspace_id": second["id"]}
        )
        assert audit_events.status_code == 200
        assert all(
            event["workspace_id"] == second["id"] for event in audit_events.json()
        )


def test_project_rejects_cross_workspace_mission_link():
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        first = client.post("/api/v1/workspaces", json={"name": "Project owner"}).json()
        second = client.post("/api/v1/workspaces", json={"name": "Other owner"}).json()
        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": first["id"],
                "name": "Scoped",
                "purpose": "Scoped test",
            },
        ).json()
        response = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": second["id"],
                "project_id": project["project_id"],
                "title": "Cross boundary",
                "objective": "Must fail closed",
            },
        )
        assert response.status_code == 404


def test_project_update_requires_current_version():
    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        workspace = client.post(
            "/api/v1/workspaces", json={"name": "Project versioning"}
        ).json()
        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": "Versioned",
                "purpose": "Prove optimistic concurrency",
            },
        ).json()
        updated = client.patch(
            f"/api/v1/projects/{project['project_id']}",
            params={"workspace_id": workspace["id"]},
            json={"state": "paused", "expected_version": 1},
        )
        assert updated.status_code == 200
        assert updated.json()["state"] == "paused"
        assert updated.json()["version"] == 2
        stale = client.patch(
            f"/api/v1/projects/{project['project_id']}",
            params={"workspace_id": workspace["id"]},
            json={"name": "Must fail", "expected_version": 1},
        )
        assert stale.status_code == 409
