"""
Agent API Routes
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..core.time import utcnow
from ..models.agent import Agent as AgentModel
from ..schemas.agent import Agent as AgentSchema
from ..schemas.agent import AgentCreate, AgentUpdate

router = APIRouter()


@router.get("", response_model=List[AgentSchema])
async def list_agents(
    limit: int = 20,
    offset: int = 0,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all agents."""
    query = select(AgentModel)
    if status:
        query = query.where(AgentModel.status == status)
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    agents = result.scalars().all()
    return agents


@router.post("", response_model=AgentSchema, status_code=201)
async def create_agent(agent: AgentCreate, db: AsyncSession = Depends(get_db)):
    """Create a new agent."""
    db_agent = AgentModel(
        name=agent.name,
        model=agent.model,
        status="active",
        description=agent.description,
        capabilities=agent.capabilities or [],
        config=agent.config or {},
        policies=agent.policies or {},
    )
    db.add(db_agent)
    await db.commit()
    await db.refresh(db_agent)
    return db_agent


@router.get("/{agent_id}", response_model=AgentSchema)
async def get_agent(agent_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get agent by ID."""
    query = select(AgentModel).where(AgentModel.id == agent_id)
    result = await db.execute(query)
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.patch("/{agent_id}", response_model=AgentSchema)
async def update_agent(
    agent_id: UUID, update: AgentUpdate, db: AsyncSession = Depends(get_db)
):
    """Update agent."""
    query = select(AgentModel).where(AgentModel.id == agent_id)
    result = await db.execute(query)
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)

    agent.updated_at = utcnow()
    await db.commit()
    await db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete agent."""
    from ..models.run import Run

    query = select(AgentModel).where(AgentModel.id == agent_id)
    result = await db.execute(query)
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    runs = (
        await db.execute(select(Run).where(Run.agent_id == agent_id).limit(1))
    ).scalar_one_or_none()
    if runs is not None:
        raise HTTPException(
            status_code=409,
            detail="Agent has existing runs; archive or remove them first",
        )

    await db.delete(agent)
    await db.commit()
