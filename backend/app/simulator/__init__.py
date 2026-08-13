"""Deterministic, credential-free adapter simulator for D0."""

from .adapter import SimulatorAdapter
from .contracts import AdapterRequest, AdapterResult, FailureKind, FixtureProfile

__all__ = [
    "AdapterRequest",
    "AdapterResult",
    "FailureKind",
    "FixtureProfile",
    "SimulatorAdapter",
]
