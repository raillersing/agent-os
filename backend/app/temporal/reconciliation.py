"""Durable dispatch reconciliation for accepted D1 runs."""

from sqlalchemy import and_, or_, select, update
from temporalio.client import Client
from temporalio.exceptions import WorkflowAlreadyStartedError

from ..config import settings
from ..core.database import AsyncSessionLocal
from ..models.control_plane import AuditEvent, ExecutionRun, TaskSnapshot
from .workflows import D1SimulatorRunInput, D1SimulatorRunWorkflow

DISPATCH_CANCELLATION_STATES = {"requested", "confirmed", "unconfirmed"}


def is_dispatch_recoverable(run: ExecutionRun) -> bool:
    """Classify only states that represent an unresolved dispatch."""
    if run.cancellation_state in DISPATCH_CANCELLATION_STATES:
        return False
    if run.state == "accepted":
        return True
    return (
        run.state == "unknown" and run.state_reason == "temporal_dispatch_unconfirmed"
    )


def dispatch_recoverable_filter(model):
    """SQL predicate matching :func:`is_dispatch_recoverable`."""
    no_cancellation = model.cancellation_state.not_in(DISPATCH_CANCELLATION_STATES)
    return or_(
        and_(model.state == "accepted", no_cancellation),
        and_(
            model.state == "unknown",
            model.state_reason == "temporal_dispatch_unconfirmed",
            no_cancellation,
        ),
    )


async def reconcile_pending_runs(client: Client) -> int:
    """Dispatch committed, non-terminal runs without requiring client retry."""
    dispatched = 0
    async with AsyncSessionLocal() as db:
        runs = (
            (
                await db.execute(
                    select(ExecutionRun).where(
                        dispatch_recoverable_filter(ExecutionRun)
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
            await db.refresh(run)
            if not is_dispatch_recoverable(run):
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
                    dispatch_recoverable_filter(ExecutionRun),
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
