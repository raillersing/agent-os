"""
Memory API Routes
"""

from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..models.memory import Memory as MemoryModel
from ..schemas.memory import Memory as MemorySchema, MemoryCreate, MemorySearchResults

router = APIRouter()


@router.post("/", response_model=MemorySchema, status_code=201)
async def create_memory(memory: MemoryCreate, db: AsyncSession = Depends(get_db)):
    """Add to memory."""
    # Check if key already exists
    query = select(MemoryModel).where(MemoryModel.key == memory.key)
    result = await db.execute(query)
    existing = result.scalar_one_or_none()

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
        await db.commit()
        await db.refresh(existing)
        return existing

    db_memory = MemoryModel(
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
    await db.commit()
    await db.refresh(db_memory)
    return db_memory


@router.get("/search", response_model=MemorySearchResults)
async def search_memory(q: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Search memory."""
    query = select(MemoryModel)
    if q:
        query = query.where(
            (MemoryModel.key.ilike(f"%{q}%")) | (MemoryModel.content.ilike(f"%{q}%"))
        )
    query = query.limit(limit)
    result = await db.execute(query)
    results = result.scalars().all()

    # Count total
    count_query = select(MemoryModel)
    if q:
        count_query = count_query.where(
            (MemoryModel.key.ilike(f"%{q}%")) | (MemoryModel.content.ilike(f"%{q}%"))
        )
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    return MemorySearchResults(results=results, total=total)


@router.get("/{key}", response_model=MemorySchema)
async def get_memory(key: str, db: AsyncSession = Depends(get_db)):
    """Get memory by key."""
    query = select(MemoryModel).where(MemoryModel.key == key)
    result = await db.execute(query)
    memory = result.scalar_one_or_none()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    # Update access stats
    memory.access_count += 1
    memory.last_accessed_at = datetime.utcnow()
    await db.commit()

    return memory


@router.delete("/{key}", status_code=204)
async def delete_memory(key: str, db: AsyncSession = Depends(get_db)):
    """Delete memory."""
    query = select(MemoryModel).where(MemoryModel.key == key)
    result = await db.execute(query)
    memory = result.scalar_one_or_none()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    await db.delete(memory)
    await db.commit()
