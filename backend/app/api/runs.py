"""
Run API Routes
"""

from typing import List, Optional
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..models.run import Run as RunModel
from ..models.agent import Agent
from ..schemas.run import Run as RunSchema, RunCreate

router = APIRouter()


@router.get("/", response_model=List[RunSchema])
async def list_runs(
    limit: int = 20,
    offset: int = 0,
    agent_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all runs."""
    query = select(RunModel)
    if agent_id:
        query = query.where(RunModel.agent_id == agent_id)
    if status:
        query = query.where(RunModel.status == status)
    query = query.order_by(RunModel.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    runs = result.scalars().all()
    return runs


@router.post("/{agent_id}/run", response_model=RunSchema, status_code=202)
async def create_run(agent_id: UUID, run: RunCreate, db: AsyncSession = Depends(get_db)):
    """Create and start a run."""
    # Verify agent exists
    query = select(Agent).where(Agent.id == agent_id)
    result = await db.execute(query)
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db_run = RunModel(
        agent_id=agent_id,
        status="pending",
        prompt=run.prompt,
        context=run.context or {},
        options=run.options or {},
        started_at=datetime.utcnow(),
    )
    db.add(db_run)
    await db.commit()
    await db.refresh(db_run)
    return db_run


@router.get("/{run_id}", response_model=RunSchema)
async def get_run(run_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get run by ID."""
    query = select(RunModel).where(RunModel.id == run_id)
    result = await db.execute(query)
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/cancel", response_model=RunSchema)
async def cancel_run(run_id: UUID, db: AsyncSession = Depends(get_db)):
    """Cancel a running run."""
    query = select(RunModel).where(RunModel.id == run_id)
    result = await db.execute(query)
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.status not in ["pending", "running"]:
        raise HTTPException(status_code=400, detail="Run cannot be cancelled")

    run.status = "cancelled"
    run.completed_at = datetime.utcnow()
    await db.commit()
    await db.refresh(run)
    return run
