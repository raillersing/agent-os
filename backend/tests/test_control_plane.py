"""Persistence and governance tests for the MVP control plane."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_workspace_mission_automation_and_approval_persist_across_clients():
    suffix = uuid4().hex[:8]

    with TestClient(app) as first_client:
        workspace_response = first_client.post(
            "/api/v1/workspaces",
            json={"name": f"Workspace {suffix}", "description": "Persistence proof", "budget": 100},
        )
        assert workspace_response.status_code == 201
        workspace = workspace_response.json()

        mission_response = first_client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
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
        workspaces = restarted_client.get("/api/v1/workspaces").json()
        assert any(item["id"] == workspace["id"] for item in workspaces)

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
            json={"status": "approved", "decision_note": "Approved for this mission only"},
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
        assert {"workspace.created", "mission.created", "automation.created", "approval.requested", "approval.approved"} <= event_types


def test_mission_rejects_unknown_workspace():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": str(uuid4()),
                "title": "Invalid mission",
                "objective": "Must not cross an unknown workspace boundary",
            },
        )
        assert response.status_code == 404


def test_workspace_filters_do_not_return_another_workspace_records():
    with TestClient(app) as client:
        first = client.post('/api/v1/workspaces', json={'name': f'First {uuid4().hex[:8]}'}).json()
        second = client.post('/api/v1/workspaces', json={'name': f'Second {uuid4().hex[:8]}'}).json()
        mission = client.post('/api/v1/missions', json={
            'workspace_id': first['id'], 'title': 'Private mission', 'objective': 'Stay scoped',
        }).json()
        automation = client.post('/api/v1/automations', json={
            'workspace_id': first['id'], 'name': 'Private automation', 'trigger_type': 'manual',
        }).json()

        assert [item['id'] for item in client.get('/api/v1/missions', params={'workspace_id': second['id']}).json()] == []
        assert [item['id'] for item in client.get('/api/v1/automations', params={'workspace_id': second['id']}).json()] == []
        assert mission['workspace_id'] == first['id']
        assert automation['workspace_id'] == first['id']

        audit_events = client.get('/api/v1/audit-events', params={'workspace_id': second['id']})
        assert audit_events.status_code == 200
        assert all(event['workspace_id'] == second['id'] for event in audit_events.json())
