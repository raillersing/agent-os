"""Provider-neutral model invocation contracts.

Provider SDK request/response classes must not cross this boundary.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ModelInvocationRequest:
    input_text: str
    system_instructions: str
    configured_model: str
    request_id: str
    output_schema: Mapping[str, Any] | None = None
    max_output_tokens: int = 256


@dataclass(frozen=True)
class UsageObservation:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cached_input_tokens: int | None = None
    source: str = "unknown"
    completeness: str = "unknown"
    raw: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelInvocationResult:
    output_text: str
    structured_result: Mapping[str, Any] | None
    adapter_id: str
    adapter_version: str
    configured_provider: str
    configured_model: str
    actual_provider: str | None
    actual_model: str | None
    identity_state: str
    provider_request_id: str | None
    response_id: str | None
    usage: UsageObservation
    stop_reason: str
    refusal_state: str
    latency_ms: int


class ModelProviderError(RuntimeError):
    """Provider-neutral error with explicit retry behavior."""

    def __init__(self, code: str, message: str, *, retryable: bool):
        super().__init__(message)
        self.code = code
        self.retryable = retryable
