"""Durable dispatch reconciliation for accepted D1 runs."""

from sqlalchemy import select, update
from temporalio.client import Client
from temporalio.exceptions import WorkflowAlreadyStartedError

from ..config import settings
from ..core.database import AsyncSessionLocal
from ..models.control_plane import AuditEvent, ExecutionRun, TaskSnapshot
from .workflows import D1SimulatorRunInput, D1SimulatorRunWorkflow


async def reconcile_pending_runs(client: Client) -> int:
    """Dispatch committed, non-terminal runs without requiring client retry."""
    dispatched = 0
    async with AsyncSessionLocal() as db:
        runs = (
            (
                await db.execute(
                    select(ExecutionRun).where(
                        ExecutionRun.state.in_(["accepted", "unknown"])
                    )
                )
            )
            .scalars()
            .all()
        )
        for run in runs:
            snapshot = await db.get(TaskSnapshot, run.task_snapshot_id)
            if snapshot is None:
                continue
            try:
                await client.start_workflow(
                    D1SimulatorRunWorkflow.run,
                    D1SimulatorRunInput(
                        str(run.id),
                        str(run.workspace_id),
                        snapshot.input_text,
                        snapshot.simulator_profile,
                    ),
                    id=run.workflow_id,
                    task_queue=settings.TEMPORAL_TASK_QUEUE,
                )
            except WorkflowAlreadyStartedError:
                pass
            except Exception:
                # The run remains accepted/unknown and is retried next tick.
                continue
            transitioned = await db.execute(
                update(ExecutionRun)
                .where(
                    ExecutionRun.id == run.id,
                    ExecutionRun.state.in_(["accepted", "unknown"]),
                )
                .values(
                    state="queued",
                    state_reason=None,
                    version=ExecutionRun.version + 1,
                )
            )
            if transitioned.rowcount:
                db.add(
                    AuditEvent(
                        workspace_id=run.workspace_id,
                        event_type="run.dispatched",
                        resource_type="execution_run",
                        resource_id=run.id,
                        details={"workflow_id": run.workflow_id, "reconciled": True},
                    )
                )
                dispatched += 1
        await db.commit()
    return dispatched
