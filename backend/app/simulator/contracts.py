"""Provider-neutral adapter contracts used by the simulator and future adapters."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class FailureKind(StrEnum):
    RETRYABLE = "retryable_failure"
    NON_RETRYABLE = "non_retryable_failure"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class FixtureProfile:
    name: str
    failure: FailureKind | None = None
    unknown_cost: bool = False


@dataclass(frozen=True)
class AdapterRequest:
    input_text: str
    profile: FixtureProfile
    metadata: Mapping[str, str] | None = None


@dataclass(frozen=True)
class AdapterResult:
    adapter_type: str
    fixture: str
    output_text: str | None
    status: str
    cost: float | None
    cost_status: str
    provider_identity: str
    retryable: bool


class AdapterError(RuntimeError):
    """Controlled adapter failure with an explicit retry classification."""

    def __init__(self, kind: FailureKind, fixture: str):
        super().__init__(f"simulator fixture {fixture}: {kind.value}")
        self.kind = kind
        self.fixture = fixture
