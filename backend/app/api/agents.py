"""
Agent API Routes
"""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.agent import Agent
from ..schemas.agent import Agent, AgentCreate, AgentUpdate

router = APIRouter()


@router.get("/", response_model=List[Agent])
async def list_agents(
    limit: int = 20,
    offset: int = 0,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all agents."""
    query = db.query(Agent)
    if status:
        query = query.filter(Agent.status == status)
    agents = query.offset(offset).limit(limit).all()
    return agents


@router.post("/", response_model=Agent, status_code=201)
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent."""
    db_agent = Agent(
        name=agent.name,
        model=agent.model,
        status="active",
        description=agent.description,
        capabilities=agent.capabilities or [],
        config=agent.config or {},
        policies=agent.policies or {},
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get agent by ID."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.patch("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, update: AgentUpdate, db: Session = Depends(get_db)):
    """Update agent."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)

    agent.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """Delete agent."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
