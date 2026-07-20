"""
Agent API Routes
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..schemas.agent import Agent, AgentCreate, AgentUpdate

router = APIRouter()

# In-memory storage for MVP
agents_db: dict[str, Agent] = {}


@router.get("/", response_model=List[Agent])
async def list_agents(
    limit: int = 20,
    offset: int = 0,
    status: Optional[str] = None,
):
    """List all agents."""
    agents = list(agents_db.values())
    if status:
        agents = [a for a in agents if a.status == status]
    return agents[offset : offset + limit]


@router.post("/", response_model=Agent, status_code=201)
async def create_agent(agent: AgentCreate):
    """Create a new agent."""
    import uuid
    from datetime import datetime

    new_agent = Agent(
        id=str(uuid.uuid4()),
        name=agent.name,
        model=agent.model,
        status="active",
        capabilities=agent.capabilities or [],
        config=agent.config or {},
        policies=agent.policies or {},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    agents_db[new_agent.id] = new_agent
    return new_agent


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get agent by ID."""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_db[agent_id]


@router.patch("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, update: AgentUpdate):
    """Update agent."""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agents_db[agent_id]
    update_data = update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(agent, field, value)

    from datetime import datetime

    agent.updated_at = datetime.utcnow()
    return agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: str):
    """Delete agent."""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agents_db[agent_id]
