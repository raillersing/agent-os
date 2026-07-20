"""
Run API Routes
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..schemas.run import Run, RunCreate

router = APIRouter()

# In-memory storage for MVP
runs_db: dict[str, Run] = {}


@router.get("/", response_model=List[Run])
async def list_runs(
    limit: int = 20,
    offset: int = 0,
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
):
    """List all runs."""
    runs = list(runs_db.values())
    if agent_id:
        runs = [r for r in runs if r.agent_id == agent_id]
    if status:
        runs = [r for r in runs if r.status == status]
    return runs[offset : offset + limit]


@router.post("/{agent_id}/run", response_model=Run, status_code=202)
async def create_run(agent_id: str, run: RunCreate):
    """Create and start a run."""
    import uuid
    from datetime import datetime

    new_run = Run(
        id=str(uuid.uuid4()),
        agent_id=agent_id,
        status="pending",
        prompt=run.prompt,
        context=run.context or {},
        options=run.options or {},
        started_at=datetime.utcnow(),
    )
    runs_db[new_run.id] = new_run
    return new_run


@router.get("/{run_id}", response_model=Run)
async def get_run(run_id: str):
    """Get run by ID."""
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs_db[run_id]


@router.post("/{run_id}/cancel", response_model=Run)
async def cancel_run(run_id: str):
    """Cancel a running run."""
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail="Run not found")

    run = runs_db[run_id]
    if run.status not in ["pending", "running"]:
        raise HTTPException(status_code=400, detail="Run cannot be cancelled")

    run.status = "cancelled"
    from datetime import datetime

    run.completed_at = datetime.utcnow()
    return run
