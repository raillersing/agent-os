#!/usr/bin/env python3
"""Opt-in, one-run OpenAI D2 smoke with durable evidence.

This script never prints credentials, prompts, model output, or raw provider
errors. It requires an already migrated Agent OS database and explicit live
execution configuration.
"""

import asyncio
import os
import sys
import uuid

from sqlalchemy import select

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "backend"))

from app.config import settings  # noqa: E402
from app.core.database import AsyncSessionLocal  # noqa: E402
from app.models.control_plane import (  # noqa: E402
    Artifact,
    ExecutionRun,
    Mission,
    ModelInvocation,
    Project,
    Task,
    TaskSnapshot,
    UsageRecord,
    Workspace,
)
from app.temporal.activities import execute_d1_simulator_run  # noqa: E402
from app.temporal.workflows import D1SimulatorRunInput  # noqa: E402


async def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("LIVE D2 smoke not run: OPENAI_API_KEY is absent")
        return 2
    if not settings.OPENAI_EXECUTION_ENABLED:
        print("LIVE D2 smoke not run: OPENAI_EXECUTION_ENABLED is false")
        return 2

    workspace_id = uuid.uuid4()
    project_id = uuid.uuid4()
    mission_id = uuid.uuid4()
    task_id = uuid.uuid4()
    snapshot_id = uuid.uuid4()
    run_id = uuid.uuid4()
    correlation_id = uuid.uuid4()
    workflow_id = f"d2-live-smoke-{run_id}"
    input_text = "Return one short answer and state uncertainty if evidence is absent."

    async with AsyncSessionLocal() as db:
        db.add(Workspace(id=workspace_id, name="D2 live smoke", budget=1.0))
        await db.flush()
        db.add(
            Project(
                project_id=project_id,
                workspace_id=workspace_id,
                name="D2 live smoke",
                purpose="Credential-gated bounded provider smoke",
                created_by=uuid.uuid4(),
            )
        )
        await db.flush()
        db.add(
            Mission(
                id=mission_id,
                workspace_id=workspace_id,
                project_id=project_id,
                title="D2 live smoke",
                objective="Validate one bounded OpenAI Responses invocation",
            )
        )
        await db.flush()
        db.add(
            Task(
                id=task_id,
                workspace_id=workspace_id,
                project_id=project_id,
                mission_id=mission_id,
                title="D2 live smoke",
                desired_outcome="Structured answer with uncertainty",
                created_by=uuid.uuid4(),
            )
        )
        await db.flush()
        db.add(
            TaskSnapshot(
                id=snapshot_id,
                task_id=task_id,
                workspace_id=workspace_id,
                input_text=input_text,
                simulator_profile="success",
                execution_mode="openai",
                model_profile="model.general.balanced",
                content_hash=__import__("hashlib")
                .sha256(input_text.encode())
                .hexdigest(),
            )
        )
        await db.flush()
        db.add(
            ExecutionRun(
                id=run_id,
                workspace_id=workspace_id,
                project_id=project_id,
                mission_id=mission_id,
                task_id=task_id,
                task_snapshot_id=snapshot_id,
                idempotency_key=f"live-{run_id}",
                request_hash=__import__("hashlib")
                .sha256(input_text.encode())
                .hexdigest(),
                correlation_id=correlation_id,
                workflow_id=workflow_id,
            )
        )
        await db.commit()

    result = await execute_d1_simulator_run(
        D1SimulatorRunInput(
            str(run_id),
            str(workspace_id),
            input_text,
            "success",
            "openai",
            "model.general.balanced",
        )
    )

    async with AsyncSessionLocal() as db:
        invocation = (
            await db.execute(
                select(ModelInvocation).where(ModelInvocation.run_id == run_id)
            )
        ).scalar_one()
        usage = (
            await db.execute(select(UsageRecord).where(UsageRecord.run_id == run_id))
        ).scalar_one()
        artifact = (
            await db.execute(select(Artifact).where(Artifact.run_id == run_id))
        ).scalar_one()
    print(
        {
            "run_id": str(run_id),
            "state": result["state"],
            "provider": invocation.actual_provider,
            "model": invocation.actual_model,
            "provider_request_id_present": bool(invocation.provider_request_id),
            "response_id_present": bool(invocation.response_id),
            "usage_source": usage.source,
            "usage_completeness": usage.completeness,
            "cost_state": usage.cost_state,
            "artifact_hash_present": bool(artifact.content_hash),
            "tools_enabled": bool(invocation.tools_enabled),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
