"""Manual validation script for a real OpenAI D2 execution run.

Usage (from backend directory):
    OPENAI_API_KEY=sk-... OPENAI_EXECUTION_ENABLED=1 .venv/bin/python scripts/validate_openai_d2.py

The script creates a workspace/project/mission/task/run, executes the D1 workflow
against a real Temporal server, and prints the resulting execution run evidence.
"""

import asyncio
from uuid import uuid4

from fastapi.testclient import TestClient
from temporalio.client import Client
from temporalio.worker import Worker

from app.config import settings
from app.main import app
from app.temporal.activities import execute_d1_simulator_run, finalize_d1_failed_run
from app.temporal.workflows import D1SimulatorRunInput, D1SimulatorRunWorkflow
from tests.conftest import auth_headers


async def _run_workflow(run_id: str, workspace_id: str) -> dict:
    client = await Client.connect(
        settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE
    )
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
                input_text="Say a short hello and report confidence as low, medium or high.",
                simulator_profile="success",
                execution_mode="openai",
                model_profile="model.general.balanced",
            ),
            id=f"validate-openai-{run_id}",
            task_queue=settings.TEMPORAL_TASK_QUEUE,
        )


def main():
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")
    if not settings.OPENAI_EXECUTION_ENABLED:
        raise RuntimeError("OPENAI_EXECUTION_ENABLED is not set to 1/true")

    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        suffix = uuid4().hex[:8]
        workspace = client.post(
            "/api/v1/workspaces",
            json={"name": f"OpenAI Validate {suffix}", "description": "D2 validation"},
        ).json()
        project = client.post(
            "/api/v1/projects",
            json={
                "workspace_id": workspace["id"],
                "name": f"Project {suffix}",
                "purpose": "D2 validation",
            },
        ).json()
        mission = client.post(
            "/api/v1/missions",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "title": f"Mission {suffix}",
                "objective": "Validate OpenAI D2 execution",
            },
        ).json()
        task = client.post(
            "/api/v1/tasks",
            json={
                "workspace_id": workspace["id"],
                "project_id": project["project_id"],
                "mission_id": mission["id"],
                "title": f"Task {suffix}",
                "desired_outcome": "Real OpenAI evidence",
            },
        ).json()
        run = client.post(
            f"/api/v1/tasks/{task['id']}/runs",
            json={
                "workspace_id": workspace["id"],
                "input_text": "Say a short hello and report confidence as low, medium or high.",
                "execution_mode": "openai",
                "model_profile": "model.general.balanced",
                "idempotency_key": f"validate-openai-{suffix}",
            },
        ).json()
        run_id = run["id"]

    result = asyncio.run(_run_workflow(run_id, workspace["id"]))
    print("Workflow result:", result)

    with TestClient(app) as client:
        client.headers.update(auth_headers(client))
        response = client.get(
            f"/api/v1/execution-runs/{run_id}",
            params={"workspace_id": workspace["id"]},
        )
        run_data = response.json()
        print("\nExecution run:")
        print(f"  state: {run_data['state']}")
        print(f"  execution_mode: {run_data['execution_mode']}")
        print(f"  model_profile: {run_data['model_profile']}")
        print(f"  attempts: {len(run_data['attempts'])}")
        if run_data["attempts"]:
            attempt = run_data["attempts"][0]
            print(f"  actual_model: {attempt.get('actual_model')}")
            print(f"  identity_state: {attempt.get('identity_state')}")
            print(f"  latency_ms: {attempt.get('latency_ms')}")
        print(f"  artifacts: {len(run_data['artifacts'])}")
        if run_data["artifacts"]:
            print(f"  artifact preview: {run_data['artifacts'][0]['content'][:200]}")
        if run_data["receipt"]:
            print(f"  receipt terminal_state: {run_data['receipt']['terminal_state']}")
            print(f"  provider_identity: {run_data['receipt']['provider_identity']}")

        evidence = client.get(
            f"/api/v1/execution-runs/{run_id}/evidence",
            params={"workspace_id": workspace["id"]},
        ).json()
        print("\nEvidence:")
        print(
            f"  disclosure_state: {evidence['context_manifests'][0]['disclosure_state']}"
        )
        print(f"  invocations: {len(evidence['invocations'])}")
        if evidence["invocations"]:
            inv = evidence["invocations"][0]
            print(f"    actual_model: {inv.get('actual_model')}")
            print(f"    latency_ms: {inv.get('latency_ms')}")
        print(f"  usage records: {len(evidence['usage'])}")
        if evidence["usage"]:
            usage = evidence["usage"][0]
            print(f"    source: {usage.get('source')}")
            print(f"    input_tokens: {usage.get('input_tokens')}")
            print(f"    output_tokens: {usage.get('output_tokens')}")


if __name__ == "__main__":
    main()
