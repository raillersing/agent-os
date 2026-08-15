"""D1 effect boundary: database persistence and simulator execution only occur here."""

import asyncio
import hashlib
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from temporalio import activity
from temporalio.exceptions import ApplicationError

from ..core.database import AsyncSessionLocal
from ..models.control_plane import (
    Artifact,
    AuditEvent,
    ExecutionReceipt,
    ExecutionRun,
    RunAttempt,
    TaskSnapshot,
)
from ..simulator import AdapterError, AdapterRequest, SimulatorAdapter
from ..simulator.fixtures import ALL_PROFILES
from .workflows import D1SimulatorRunInput

PROFILES = {profile.name: profile for profile in ALL_PROFILES}


async def _terminal_result(
    db, run: ExecutionRun, receipt: ExecutionReceipt | None
) -> dict[str, str] | None:
    """Return durable terminal evidence without creating new business facts."""
    terminal_states = {"completed", "failed", "cancelled"}
    state = receipt.terminal_state if receipt is not None else run.state
    if state not in terminal_states:
        return None
    artifact = None
    if receipt is not None and receipt.artifact_id:
        artifact = await db.get(Artifact, receipt.artifact_id)
    return {
        "run_id": str(run.id),
        "state": state,
        "artifact_hash": artifact.content_hash if artifact else "",
    }


@activity.defn(name="finalize_d1_failed_run")
async def finalize_d1_failed_run(run_id: str) -> dict[str, str]:
    async with AsyncSessionLocal() as db:
        run = await db.get(ExecutionRun, UUID(run_id))
        if run is None:
            raise ApplicationError("run unavailable", non_retryable=True)
        existing_receipt = (
            await db.execute(
                select(ExecutionReceipt).where(ExecutionReceipt.run_id == run.id)
            )
        ).scalar_one_or_none()
        terminal = await _terminal_result(db, run, existing_receipt)
        if terminal is not None:
            return {"run_id": run_id, "state": terminal["state"]}
        run.state, run.ended_at, run.receipt_state, run.version = (
            "failed",
            datetime.utcnow(),
            "available",
            run.version + 1,
        )
        if existing_receipt is None:
            snapshot = await db.get(TaskSnapshot, run.task_snapshot_id)
            attempt = (
                (
                    await db.execute(
                        select(RunAttempt)
                        .where(RunAttempt.run_id == run.id)
                        .order_by(RunAttempt.attempt_number.desc())
                    )
                )
                .scalars()
                .first()
            )
            db.add(
                ExecutionReceipt(
                    workspace_id=run.workspace_id,
                    run_id=run.id,
                    attempt_id=attempt.id if attempt else None,
                    terminal_state="failed",
                    reason_code=run.state_reason or "retry_exhausted",
                    simulator_identity="simulator/d0",
                    input_hash=snapshot.content_hash if snapshot else "unknown",
                )
            )
        db.add(
            AuditEvent(
                workspace_id=run.workspace_id,
                event_type="run.failed",
                resource_type="execution_run",
                resource_id=run.id,
                details={"reason": run.state_reason or "retry_exhausted"},
            )
        )
        await db.commit()
        return {"run_id": run_id, "state": "failed"}


@activity.defn(name="execute_d1_simulator_run")
async def execute_d1_simulator_run(request: D1SimulatorRunInput) -> dict[str, str]:
    """Create immutable attempt/evidence records and execute the local simulator."""
    async with AsyncSessionLocal() as db:
        run = await db.get(ExecutionRun, UUID(request.run_id))
        snapshot = await db.get(TaskSnapshot, run.task_snapshot_id) if run else None
        if (
            run is None
            or snapshot is None
            or str(run.workspace_id) != request.workspace_id
        ):
            raise ApplicationError(
                "run unavailable", non_retryable=True, type="InvalidRun"
            )
        existing_receipt = (
            await db.execute(
                select(ExecutionReceipt).where(ExecutionReceipt.run_id == run.id)
            )
        ).scalar_one_or_none()
        terminal = await _terminal_result(db, run, existing_receipt)
        if terminal is not None:
            return terminal
        run.state, run.started_at, run.version = (
            "running",
            datetime.utcnow(),
            run.version + 1,
        )
        db.add(
            AuditEvent(
                workspace_id=run.workspace_id,
                event_type="run.started",
                resource_type="execution_run",
                resource_id=run.id,
                details={"workflow_id": run.workflow_id},
            )
        )
        previous_attempts = (
            (
                await db.execute(
                    select(RunAttempt).where(
                        RunAttempt.run_id == run.id, RunAttempt.state == "running"
                    )
                )
            )
            .scalars()
            .all()
        )
        for previous in previous_attempts:
            (
                previous.state,
                previous.failure_kind,
                previous.side_effect_certainty,
                previous.ended_at,
            ) = ("unknown", "worker_interrupted", "unknown", datetime.utcnow())
            db.add(
                AuditEvent(
                    workspace_id=run.workspace_id,
                    event_type="run.attempt_unknown",
                    resource_type="run_attempt",
                    resource_id=previous.id,
                    details={"reason": "worker_interrupted"},
                )
            )
        count = await db.scalar(
            select(func.count())
            .select_from(RunAttempt)
            .where(RunAttempt.run_id == run.id)
        )
        attempt = RunAttempt(
            run_id=run.id,
            workspace_id=run.workspace_id,
            attempt_number=(count or 0) + 1,
            idempotency_key=f"{run.id}:{(count or 0) + 1}",
            state="running",
            provider_identity="simulator/d0",
            side_effect_certainty="none",
        )
        db.add(attempt)
        await db.commit()
        await db.refresh(attempt)
        try:
            if request.simulator_profile == "slow_success":
                for _ in range(40):
                    activity.heartbeat({"phase": "slow_simulator", "remaining": 40 - _})
                    await asyncio.sleep(0.5)
            result = SimulatorAdapter().execute(
                AdapterRequest(request.input_text, PROFILES[request.simulator_profile])
            )
        except AdapterError as error:
            attempt.state, attempt.failure_kind, attempt.ended_at = (
                "failed",
                error.kind.value,
                datetime.utcnow(),
            )
            if error.kind.value == "retryable_failure":
                run.state, run.state_reason, run.version = (
                    "retrying",
                    error.kind.value,
                    run.version + 1,
                )
                db.add(
                    AuditEvent(
                        workspace_id=run.workspace_id,
                        event_type="run.retry_scheduled",
                        resource_type="execution_run",
                        resource_id=run.id,
                        details={
                            "attempt_number": attempt.attempt_number,
                            "reason": error.kind.value,
                        },
                    )
                )
                await db.commit()
                raise ApplicationError(str(error), type="RetryableSimulatorError")
            run.state, run.state_reason, run.ended_at, run.version = (
                "failed",
                error.kind.value,
                datetime.utcnow(),
                run.version + 1,
            )
            receipt = ExecutionReceipt(
                workspace_id=run.workspace_id,
                run_id=run.id,
                attempt_id=attempt.id,
                terminal_state="failed",
                reason_code=error.kind.value,
                simulator_identity="simulator/d0",
                input_hash=snapshot.content_hash,
            )
            db.add(receipt)
            db.add(
                AuditEvent(
                    workspace_id=run.workspace_id,
                    event_type="run.failed",
                    resource_type="execution_run",
                    resource_id=run.id,
                    details={
                        "attempt_number": attempt.attempt_number,
                        "reason": error.kind.value,
                    },
                )
            )
            await db.commit()
            raise ApplicationError(
                str(error), non_retryable=True, type="NonRetryableSimulatorError"
            )
        # Cancellation or another terminal reconciliation may have committed
        # while the simulator was executing. Re-read durable state before
        # materializing any attempt, artifact, receipt, or terminal audit.
        await db.refresh(run)
        existing_receipt = (
            await db.execute(
                select(ExecutionReceipt).where(ExecutionReceipt.run_id == run.id)
            )
        ).scalar_one_or_none()
        terminal = await _terminal_result(db, run, existing_receipt)
        if terminal is not None:
            return terminal
        output_hash = hashlib.sha256(result.output_text.encode()).hexdigest()
        attempt.state, attempt.ended_at = "succeeded", datetime.utcnow()
        artifact = Artifact(
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            media_type="text/plain",
            content=result.output_text,
            content_hash=output_hash,
        )
        db.add(artifact)
        await db.flush()
        (
            run.state,
            run.state_reason,
            run.ended_at,
            run.last_reliable_evidence_at,
            run.receipt_state,
            run.version,
        ) = (
            "completed",
            None,
            datetime.utcnow(),
            datetime.utcnow(),
            "available",
            run.version + 1,
        )
        receipt = ExecutionReceipt(
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            artifact_id=artifact.id,
            terminal_state="completed",
            simulator_identity=result.provider_identity,
            input_hash=snapshot.content_hash,
            output_hash=output_hash,
        )
        db.add(receipt)
        await db.flush()
        db.add(
            AuditEvent(
                workspace_id=run.workspace_id,
                event_type="artifact.created",
                resource_type="artifact",
                resource_id=artifact.id,
                details={"run_id": str(run.id), "content_hash": output_hash},
            )
        )
        db.add(
            AuditEvent(
                workspace_id=run.workspace_id,
                event_type="run.completed",
                resource_type="execution_run",
                resource_id=run.id,
                details={
                    "attempt_number": attempt.attempt_number,
                    "receipt_id": str(receipt.id),
                },
            )
        )
        await db.commit()
        return {
            "run_id": str(run.id),
            "state": "completed",
            "artifact_hash": output_hash,
        }
