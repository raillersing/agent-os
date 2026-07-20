"""
Memory API Routes
"""

from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.memory import Memory
from ..schemas.memory import Memory, MemoryCreate, MemorySearchResults

router = APIRouter()


@router.post("/", response_model=Memory, status_code=201)
async def create_memory(memory: MemoryCreate, db: Session = Depends(get_db)):
    """Add to memory."""
    # Check if key already exists
    existing = db.query(Memory).filter(Memory.key == memory.key).first()
    if existing:
        # Update existing memory
        existing.content = memory.content
        existing.type = memory.type
        existing.source = memory.source
        existing.agent_id = memory.agent_id
        existing.metadata_ = memory.metadata_ or {}
        existing.updated_at = datetime.utcnow()
        if memory.ttl:
            existing.expires_at = datetime.utcnow() + timedelta(seconds=memory.ttl)
        db.commit()
        db.refresh(existing)
        return existing

    db_memory = Memory(
        key=memory.key,
        content=memory.content,
        type=memory.type or "knowledge",
        source=memory.source,
        agent_id=memory.agent_id,
        metadata_=memory.metadata_ or {},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=memory.ttl) if memory.ttl else None,
    )
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory


@router.get("/search", response_model=MemorySearchResults)
async def search_memory(q: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search memory."""
    query = db.query(Memory)
    if q:
        query = query.filter(
            (Memory.key.ilike(f"%{q}%")) | (Memory.content.ilike(f"%{q}%"))
        )
    results = query.limit(limit).all()
    total = query.count()
    return MemorySearchResults(results=results, total=total)


@router.get("/{key}", response_model=Memory)
async def get_memory(key: str, db: Session = Depends(get_db)):
    """Get memory by key."""
    memory = db.query(Memory).filter(Memory.key == key).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    # Update access stats
    memory.access_count += 1
    memory.last_accessed_at = datetime.utcnow()
    db.commit()

    return memory


@router.delete("/{key}", status_code=204)
async def delete_memory(key: str, db: Session = Depends(get_db)):
    """Delete memory."""
    memory = db.query(Memory).filter(Memory.key == key).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    db.delete(memory)
    db.commit()
