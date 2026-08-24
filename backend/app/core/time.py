"""Timezone-aware UTC helpers."""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current time in UTC with an explicit timezone."""
    return datetime.now(timezone.utc)
