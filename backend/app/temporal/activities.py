"""D1 effect boundary: database persistence and simulator execution only occur here."""

import asyncio
import hashlib
from uuid import UUID, uuid4

from sqlalchemy import func, select
from temporalio import activity
from temporalio.exceptions import ApplicationError

from ..config import settings
from ..context.manifest import assemble_context
from ..core.database import AsyncSessionLocal
from ..core.time import utcnow
from ..models.control_plane import (
    Artifact,
    AuditEvent,
    ContextManifest,
    ExecutionReceipt,
    ExecutionRun,
    ModelInvocation,
    RunAttempt,
    TaskSnapshot,
    UsageRecord,
    Workspace,
)
from ..providers.contracts import ModelInvocationRequest, ModelProviderError
from ..providers.openai_responses import OpenAIResponsesAdapter
from ..simulator import AdapterError, AdapterRequest, SimulatorAdapter
from ..simulator.fixtures import ALL_PROFILES
from .workflows import D1SimulatorRunInput

PROFILES = {profile.name: profile for profile in ALL_PROFILES}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "uncertainty": {"type": "string"},
    },
    "required": ["answer", "uncertainty"],
    "additionalProperties": False,
}


def _safe_heartbeat(details: dict) -> None:
    """Emit a Temporal heartbeat when running inside an activity context.

    Unit tests invoke the activity directly outside of a workflow, so a
    missing activity context must be tolerated rather than failing the call.
    """
    try:
        activity.heartbeat(details)
    except RuntimeError:
        pass


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
            utcnow(),
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
            utcnow(),
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
            ) = ("unknown", "worker_interrupted", "unknown", utcnow())
            db.add(
                AuditEvent(
                    workspace_id=run.workspace_id,
                    event_type="run.attempt_unknown",
                    resource_type="run_attempt",
                    resource_id=previous.id,
                    details={"reason": "worker_interrupted"},
                )
            )
            previous_invocation = (
                await db.execute(
                    select(ModelInvocation).where(
                        ModelInvocation.attempt_id == previous.id
                    )
                )
            ).scalar_one_or_none()
            if (
                previous_invocation is not None
                and previous_invocation.invocation_state
                not in {
                    "completed",
                    "failed",
                    "blocked",
                }
            ):
                previous_invocation.invocation_state = "unknown"
                previous_invocation.identity_state = "unavailable"
            previous_usage = (
                await db.execute(
                    select(UsageRecord).where(UsageRecord.attempt_id == previous.id)
                )
            ).scalar_one_or_none()
            if previous_usage is not None:
                previous_usage.source = "unknown"
                previous_usage.completeness = "unknown"
                previous_usage.cost_state = "unknown"
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
        context = assemble_context(
            workspace_id=str(run.workspace_id),
            input_text=snapshot.input_text,
            model_profile=getattr(snapshot, "model_profile", "model.general.balanced"),
            mission_id=str(run.mission_id),
            task_id=str(run.task_id),
            max_input_chars=settings.D2_MAX_INPUT_CHARS,
            max_output_tokens=settings.D2_MAX_OUTPUT_TOKENS,
        )
        manifest = ContextManifest(
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            context_profile_id="ctx.d2.text_generation",
            context_profile_version="1.0.0",
            segments=context.segments,
            system_instruction_hash=context.system_instruction_hash,
            rendered_input_hash=context.rendered_input_hash,
            manifest_hash=context.manifest_hash,
            disclosure_state=(
                "external_openai_experimental"
                if request.execution_mode == "openai"
                else "local_simulator"
            ),
            token_budget=context.token_budget,
            transformations=context.transformations,
        )
        db.add(manifest)
        await db.flush()
        attempt.context_manifest_id = manifest.id
        await db.commit()
        invocation = ModelInvocation(
            id=uuid4(),
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            context_manifest_id=manifest.id,
            adapter_id=(
                "openai.responses"
                if request.execution_mode == "openai"
                else "simulator"
            ),
            adapter_version="1" if request.execution_mode == "openai" else "d0",
            logical_model_profile=snapshot.model_profile,
            configured_provider=(
                "openai" if request.execution_mode == "openai" else "simulator"
            ),
            configured_model=(
                settings.OPENAI_MODEL
                if request.execution_mode == "openai"
                else "simulator/d0"
            ),
            actual_provider=None,
            actual_model=None,
            identity_state="not_started",
            provider_request_id=(
                str(run.workflow_id) if request.execution_mode == "openai" else None
            ),
            response_id=None,
            prompt_hash=context.rendered_input_hash,
            runtime_version=settings.VERSION,
            workflow_version="d2-model-v1",
            policy_version="d2-policy-v1",
            invocation_state="prepared",
            stop_reason="not_started",
            refusal_state="unknown",
            tools_enabled=0,
            latency_ms=None,
        )
        usage_record = UsageRecord(
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            source="unknown",
            completeness="unknown",
            raw_usage={},
            pricing_profile_version="unknown",
            currency="USD",
            cost_state="unknown",
        )
        db.add(invocation)
        db.add(usage_record)
        db.add(
            AuditEvent(
                workspace_id=run.workspace_id,
                event_type="model.invocation_prepared",
                resource_type="model_invocation",
                resource_id=invocation.id,
                details={
                    "attempt_id": str(attempt.id),
                    "adapter_id": invocation.adapter_id,
                    "tools_enabled": False,
                },
            )
        )
        await db.commit()
        try:
            workspace = await db.get(Workspace, run.workspace_id)
            if workspace is not None and workspace.budget > 0:
                if workspace.spent >= workspace.budget:
                    raise ModelProviderError(
                        "MODEL_BUDGET_EXHAUSTED",
                        "Workspace budget is exhausted",
                        retryable=False,
                    )
            if request.execution_mode == "openai":
                if len(snapshot.input_text) > settings.D2_MAX_INPUT_CHARS:
                    raise ModelProviderError(
                        "MODEL_INPUT_LIMIT_EXCEEDED",
                        "D2 input limit exceeded",
                        retryable=False,
                    )
                if (
                    settings.D2_RUN_BUDGET_USD is not None
                    and settings.D2_RUN_BUDGET_USD <= 0
                ):
                    raise ModelProviderError(
                        "MODEL_BUDGET_EXHAUSTED",
                        "D2 run budget is exhausted",
                        retryable=False,
                    )
                invocation.invocation_state = "request_sent"
                invocation.identity_state = "request_sent"
                attempt.side_effect_certainty = "unknown"
                manifest.token_budget = {
                    **manifest.token_budget,
                    "budget_decision": "approved_bounded",
                }
                await db.commit()
                _safe_heartbeat(
                    {
                        "phase": "openai_request",
                        "request_id": str(run.workflow_id),
                    }
                )
                model_result = await OpenAIResponsesAdapter().invoke(
                    ModelInvocationRequest(
                        input_text=context.input_text,
                        system_instructions=context.system_instructions,
                        configured_model=settings.OPENAI_MODEL,
                        request_id=str(run.workflow_id),
                        output_schema=OUTPUT_SCHEMA,
                        max_output_tokens=settings.D2_MAX_OUTPUT_TOKENS,
                    )
                )
                if model_result.identity_state == "unexpected":
                    raise ModelProviderError(
                        "MODEL_IDENTITY_UNEXPECTED",
                        "Provider identity did not match the configured boundary",
                        retryable=False,
                    )
                output_text = model_result.output_text
                provider_identity = (
                    f"{model_result.actual_provider}/{model_result.actual_model}"
                    if model_result.actual_provider and model_result.actual_model
                    else "openai/unknown"
                )
                usage = model_result.usage
                invocation.adapter_id = model_result.adapter_id
                invocation.adapter_version = model_result.adapter_version
                invocation.configured_provider = model_result.configured_provider
                invocation.configured_model = model_result.configured_model
                invocation.actual_provider = model_result.actual_provider
                invocation.actual_model = model_result.actual_model
                invocation.identity_state = model_result.identity_state
                invocation.provider_request_id = model_result.provider_request_id
                invocation.response_id = model_result.response_id
                invocation.invocation_state = "response_received"
                invocation.stop_reason = model_result.stop_reason
                invocation.refusal_state = model_result.refusal_state
                invocation.latency_ms = model_result.latency_ms
                usage_record.source = usage.source
                usage_record.completeness = usage.completeness
                usage_record.input_tokens = usage.input_tokens
                usage_record.output_tokens = usage.output_tokens
                usage_record.total_tokens = usage.total_tokens
                usage_record.cached_input_tokens = usage.cached_input_tokens
                usage_record.raw_usage = dict(usage.raw)
            else:
                if request.simulator_profile == "slow_success":
                    for _ in range(40):
                        _safe_heartbeat(
                            {"phase": "slow_simulator", "remaining": 40 - _}
                        )
                        await asyncio.sleep(0.5)
                result = SimulatorAdapter().execute(
                    AdapterRequest(
                        request.input_text, PROFILES[request.simulator_profile]
                    )
                )
                output_text = result.output_text
                provider_identity = result.provider_identity
                usage = type(
                    "SimulatorUsage",
                    (),
                    {
                        "source": "unknown",
                        "completeness": "unknown",
                        "input_tokens": None,
                        "output_tokens": None,
                        "total_tokens": None,
                        "cached_input_tokens": None,
                        "raw": {},
                    },
                )()
                invocation.actual_provider = "simulator"
                invocation.actual_model = "d0"
                invocation.identity_state = "synthetic"
                invocation.invocation_state = "response_received"
                invocation.stop_reason = result.status
                usage_record.source = usage.source
                usage_record.completeness = usage.completeness
                usage_record.cost_state = result.cost_status
                usage_record.measured_cost = result.cost
        except ModelProviderError as error:
            invocation.invocation_state = (
                "blocked"
                if error.code
                in {"MODEL_BUDGET_EXHAUSTED", "MODEL_INPUT_LIMIT_EXCEEDED"}
                else "failed"
            )
            invocation.error_code = error.code
            invocation.identity_state = "unavailable"
            usage_record.source = (
                "policy"
                if error.code
                in {"MODEL_BUDGET_EXHAUSTED", "MODEL_INPUT_LIMIT_EXCEEDED"}
                else "unknown"
            )
            usage_record.completeness = "unknown"
            manifest.token_budget = {
                **manifest.token_budget,
                "budget_decision": (
                    "blocked_exhausted"
                    if error.code == "MODEL_BUDGET_EXHAUSTED"
                    else (
                        "blocked_input_limit"
                        if error.code == "MODEL_INPUT_LIMIT_EXCEEDED"
                        else "not_applicable"
                    )
                ),
            }
            if error.code in {"MODEL_BUDGET_EXHAUSTED", "MODEL_INPUT_LIMIT_EXCEEDED"}:
                attempt.side_effect_certainty = "none"
            elif error.retryable or error.code not in {
                "MODEL_AUTHENTICATION_FAILED",
                "MODEL_EXECUTION_DISABLED",
                "MODEL_RESPONSE_INVALID",
                "MODEL_IDENTITY_UNEXPECTED",
            }:
                attempt.side_effect_certainty = "unknown"
            (
                attempt.state,
                attempt.failure_kind,
                attempt.ended_at,
                attempt.terminal_reason,
            ) = (
                "failed",
                error.code,
                utcnow(),
                error.code,
            )
            run.state, run.state_reason, run.ended_at, run.version = (
                "retrying" if error.retryable else "failed",
                error.code,
                None if error.retryable else utcnow(),
                run.version + 1,
            )
            if not error.retryable:
                db.add(
                    ExecutionReceipt(
                        workspace_id=run.workspace_id,
                        run_id=run.id,
                        attempt_id=attempt.id,
                        terminal_state="failed",
                        reason_code=error.code,
                        simulator_identity="d2/provider",
                        provider_identity="openai",
                        input_hash=snapshot.content_hash,
                    )
                )
            db.add(
                AuditEvent(
                    workspace_id=run.workspace_id,
                    event_type="model.invocation_failed",
                    resource_type="execution_run",
                    resource_id=run.id,
                    details={"error_code": error.code, "retryable": error.retryable},
                )
            )
            await db.commit()
            raise ApplicationError(
                error.code,
                non_retryable=not error.retryable,
                type=(
                    "NonRetryableModelProviderError"
                    if not error.retryable
                    else "RetryableModelProviderError"
                ),
            )
        except AdapterError as error:
            invocation.invocation_state = "failed"
            invocation.error_code = error.kind.value
            invocation.identity_state = "synthetic"
            usage_record.source = "unknown"
            usage_record.completeness = "unknown"
            attempt.state, attempt.failure_kind, attempt.ended_at = (
                "failed",
                error.kind.value,
                utcnow(),
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
                utcnow(),
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
        output_hash = hashlib.sha256(output_text.encode()).hexdigest()
        invocation.invocation_state = "completed"
        invocation.error_code = None
        attempt.provider_identity = provider_identity
        attempt.adapter_id = (
            "openai.responses" if request.execution_mode == "openai" else "simulator"
        )
        attempt.adapter_version = "1" if request.execution_mode == "openai" else "d0"
        attempt.logical_model_profile = snapshot.model_profile
        attempt.configured_provider = (
            "openai" if request.execution_mode == "openai" else "simulator"
        )
        attempt.configured_model = (
            settings.OPENAI_MODEL
            if request.execution_mode == "openai"
            else "simulator/d0"
        )
        attempt.actual_provider = (
            "openai" if request.execution_mode == "openai" else "simulator"
        )
        attempt.actual_model = (
            getattr(model_result, "actual_model", None)
            if request.execution_mode == "openai"
            else "d0"
        )
        attempt.actual_identity_state = (
            getattr(model_result, "identity_state", "synthetic")
            if request.execution_mode == "openai"
            else "synthetic"
        )
        attempt.provider_request_id = (
            getattr(model_result, "provider_request_id", None)
            if request.execution_mode == "openai"
            else None
        )
        attempt.response_id = (
            getattr(model_result, "response_id", None)
            if request.execution_mode == "openai"
            else None
        )
        attempt.usage_source = usage.source
        attempt.input_tokens = usage.input_tokens
        attempt.output_tokens = usage.output_tokens
        attempt.total_tokens = usage.total_tokens
        attempt.cached_input_tokens = usage.cached_input_tokens
        attempt.cost_state = (
            "unknown" if request.execution_mode == "openai" else result.cost_status
        )
        attempt.cost_amount = (
            None if request.execution_mode == "openai" else result.cost
        )
        attempt.latency_ms = (
            getattr(model_result, "latency_ms", None)
            if request.execution_mode == "openai"
            else None
        )
        attempt.terminal_reason = "completed"
        attempt.state, attempt.ended_at = "succeeded", utcnow()
        artifact = Artifact(
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            media_type="text/plain",
            content=output_text,
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
            utcnow(),
            utcnow(),
            "available",
            run.version + 1,
        )
        receipt = ExecutionReceipt(
            workspace_id=run.workspace_id,
            run_id=run.id,
            attempt_id=attempt.id,
            artifact_id=artifact.id,
            terminal_state="completed",
            simulator_identity=(
                result.provider_identity
                if request.execution_mode != "openai"
                else "d2/provider"
            ),
            provider_identity=provider_identity,
            input_hash=snapshot.content_hash,
            output_hash=output_hash,
        )
        db.add(receipt)
        await db.flush()

        # Update workspace spend with a bounded cost estimate.
        workspace = await db.get(Workspace, run.workspace_id)
        if workspace is not None:
            measured_cost = (
                usage_record.measured_cost
                if request.execution_mode != "openai"
                else None
            )
            estimated_cost = measured_cost or 0.0
            workspace.spent = (workspace.spent or 0.0) + estimated_cost
            workspace.updated_at = utcnow()
            db.add(workspace)
            await db.flush()

        db.add(
            AuditEvent(
                workspace_id=run.workspace_id,
                event_type="model.invocation_completed",
                resource_type="model_invocation",
                resource_id=invocation.id,
                details={
                    "provider": provider_identity,
                    "latency_ms": invocation.latency_ms,
                    "usage_source": usage_record.source,
                    "cost_state": usage_record.cost_state,
                },
            )
        )
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
                    "provider": provider_identity,
                },
            )
        )
        await db.commit()
        return {
            "run_id": str(run.id),
            "state": "completed",
            "artifact_hash": output_hash,
        }
