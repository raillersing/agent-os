"""
Run API Routes
"""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.run import Run
from ..schemas.run import Run, RunCreate

router = APIRouter()


@router.get("/", response_model=List[Run])
async def list_runs(
    limit: int = 20,
    offset: int = 0,
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all runs."""
    query = db.query(Run)
    if agent_id:
        query = query.filter(Run.agent_id == agent_id)
    if status:
        query = query.filter(Run.status == status)
    runs = query.order_by(Run.created_at.desc()).offset(offset).limit(limit).all()
    return runs


@router.post("/{agent_id}/run", response_model=Run, status_code=202)
async def create_run(agent_id: str, run: RunCreate, db: Session = Depends(get_db)):
    """Create and start a run."""
    # Verify agent exists
    from ..models.agent import Agent
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db_run = Run(
        agent_id=agent_id,
        status="pending",
        prompt=run.prompt,
        context=run.context or {},
        options=run.options or {},
        started_at=datetime.utcnow(),
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


@router.get("/{run_id}", response_model=Run)
async def get_run(run_id: str, db: Session = Depends(get_db)):
    """Get run by ID."""
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/cancel", response_model=Run)
async def cancel_run(run_id: str, db: Session = Depends(get_db)):
    """Cancel a running run."""
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.status not in ["pending", "running"]:
        raise HTTPException(status_code=400, detail="Run cannot be cancelled")

    run.status = "cancelled"
    run.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run
