"""
Memory API Routes
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..schemas.memory import Memory, MemoryCreate, MemorySearchResults

router = APIRouter()

# In-memory storage for MVP
memory_db: dict[str, Memory] = {}


@router.post("/", response_model=Memory, status_code=201)
async def create_memory(memory: MemoryCreate):
    """Add to memory."""
    import uuid
    from datetime import datetime, timedelta

    new_memory = Memory(
        key=memory.key,
        content=memory.content,
        metadata=memory.metadata or {},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=memory.ttl) if memory.ttl else None,
    )
    memory_db[new_memory.key] = new_memory
    return new_memory


@router.get("/search", response_model=MemorySearchResults)
async def search_memory(q: str, limit: int = 10):
    """Search memory."""
    results = []
    for memory in memory_db.values():
        if q.lower() in memory.content.lower() or q.lower() in memory.key.lower():
            results.append(memory)
    return MemorySearchResults(results=results[:limit], total=len(results))


@router.get("/{key}", response_model=Memory)
async def get_memory(key: str):
    """Get memory by key."""
    if key not in memory_db:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory_db[key]


@router.delete("/{key}", status_code=204)
async def delete_memory(key: str):
    """Delete memory."""
    if key not in memory_db:
        raise HTTPException(status_code=404, detail="Memory not found")
    del memory_db[key]
