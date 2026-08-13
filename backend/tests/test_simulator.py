"""D0 simulator contract and security-boundary tests."""

import pytest

from app.simulator.adapter import SimulatorAdapter
from app.simulator.contracts import AdapterError, AdapterRequest, FailureKind
from app.simulator.fixtures import ALL_PROFILES, SUCCESS, UNKNOWN_COST


def test_simulator_is_deterministic_and_explicitly_synthetic():
    adapter = SimulatorAdapter()
    request = AdapterRequest("same input", SUCCESS)

    first = adapter.execute(request)
    second = adapter.execute(request)

    assert first == second
    assert first.adapter_type == "simulator"
    assert first.provider_identity == "simulator/d0"
    assert first.cost == 0.0


def test_unknown_cost_is_not_coerced_to_zero():
    result = SimulatorAdapter().execute(AdapterRequest("input", UNKNOWN_COST))
    assert result.cost is None
    assert result.cost_status == "unknown"


@pytest.mark.parametrize("profile", ALL_PROFILES[1:4])
def test_simulator_failures_are_explicitly_classified(profile):
    with pytest.raises(AdapterError) as error:
        SimulatorAdapter().execute(AdapterRequest("input", profile))
    assert error.value.kind in {
        FailureKind.RETRYABLE,
        FailureKind.NON_RETRYABLE,
        FailureKind.TIMEOUT,
    }
