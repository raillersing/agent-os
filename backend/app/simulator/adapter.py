"""Deterministic local adapter; it never performs network or provider I/O."""

from .contracts import AdapterError, AdapterRequest, AdapterResult


class SimulatorAdapter:
    """A contract-compatible adapter with explicit synthetic identity."""

    adapter_type = "simulator"
    provider_identity = "simulator/d0"

    def execute(self, request: AdapterRequest) -> AdapterResult:
        profile = request.profile
        if profile.failure is not None:
            raise AdapterError(profile.failure, profile.name)
        return AdapterResult(
            adapter_type=self.adapter_type,
            fixture=profile.name,
            output_text=f"SIMULATOR[{profile.name}]: {request.input_text}",
            status="completed",
            cost=None if profile.unknown_cost else 0.0,
            cost_status="unknown" if profile.unknown_cost else "measured",
            provider_identity=self.provider_identity,
            retryable=False,
        )
