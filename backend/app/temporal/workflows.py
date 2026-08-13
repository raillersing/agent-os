"""Deterministic Temporal workflows. Activities are the only effect boundary."""

from dataclasses import dataclass

from temporalio import workflow


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
