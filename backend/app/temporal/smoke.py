"""Execute one D0 Temporal smoke workflow against the configured server."""

import argparse
import asyncio
from uuid import uuid4

from temporalio.client import Client

from ..config import settings
from .workflows import D0TemporalSmokeWorkflow, SmokeInput


async def run_smoke(run_id: str, payload: str) -> dict[str, str]:
    """Submit a deterministic, side-effect-free workflow to Temporal."""
    client = await Client.connect(
        settings.TEMPORAL_ADDRESS, namespace=settings.TEMPORAL_NAMESPACE
    )
    return await client.execute_workflow(
        D0TemporalSmokeWorkflow.run,
        SmokeInput(run_id=run_id, payload=payload),
        id=f"d0-temporal-smoke-{run_id}",
        task_queue=settings.TEMPORAL_TASK_QUEUE,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=uuid4().hex)
    parser.add_argument("--payload", default="d0-smoke")
    args = parser.parse_args()
    print(asyncio.run(run_smoke(args.run_id, args.payload)))


if __name__ == "__main__":
    main()
