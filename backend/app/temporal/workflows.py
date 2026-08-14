"""Deterministic Temporal workflows. Activities are the only effect boundary."""

from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, CancelledError


@dataclass(frozen=True)
class SmokeInput:
    run_id: str
    payload: str


@workflow.defn
class D0TemporalSmokeWorkflow:
    """Minimal durable workflow used for local smoke and recovery checks."""

    @workflow.run
    async def run(self, request: SmokeInput) -> dict[str, str]:
        # Deliberately deterministic: no clock, randomness, DB, network, or provider.
        return {
            "run_id": request.run_id,
            "status": "completed",
            "workflow": "d0-temporal-smoke",
            "payload": request.payload,
        }


@dataclass(frozen=True)
class D1SimulatorRunInput:
    run_id: str
    workspace_id: str
    input_text: str
    simulator_profile: str


@workflow.defn
class D1SimulatorRunWorkflow:
    """Deterministic orchestration; all persistence and simulator calls are Activities."""

    @workflow.run
    async def run(self, request: D1SimulatorRunInput) -> dict[str, str]:
        try:
            return await workflow.execute_activity(
                "execute_d1_simulator_run",
                request,
                start_to_close_timeout=timedelta(seconds=30),
                heartbeat_timeout=timedelta(seconds=2),
                retry_policy=RetryPolicy(
                    maximum_attempts=2,
                    non_retryable_error_types=[
                        "NonRetryableSimulatorError",
                        "SimulatorTimeoutError",
                    ],
                ),
            )
        except ActivityError as error:
            if isinstance(error.cause, CancelledError):
                raise
            return await workflow.execute_activity(
                "finalize_d1_failed_run",
                request.run_id,
                start_to_close_timeout=timedelta(seconds=30),
            )
        except CancelledError:
            raise
        except Exception:
            return await workflow.execute_activity(
                "finalize_d1_failed_run",
                request.run_id,
                start_to_close_timeout=timedelta(seconds=30),
            )
