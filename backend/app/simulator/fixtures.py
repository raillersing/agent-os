"""Stable D0 simulator profiles."""

from .contracts import FailureKind, FixtureProfile

SUCCESS = FixtureProfile("success")
RETRYABLE_FAILURE = FixtureProfile("retryable_failure", FailureKind.RETRYABLE)
NON_RETRYABLE_FAILURE = FixtureProfile(
    "non_retryable_failure", FailureKind.NON_RETRYABLE
)
TIMEOUT = FixtureProfile("timeout", FailureKind.TIMEOUT)
UNKNOWN_COST = FixtureProfile("unknown_cost", unknown_cost=True)
SLOW_SUCCESS = FixtureProfile("slow_success")

ALL_PROFILES = (
    SUCCESS,
    RETRYABLE_FAILURE,
    NON_RETRYABLE_FAILURE,
    TIMEOUT,
    UNKNOWN_COST,
    SLOW_SUCCESS,
)
