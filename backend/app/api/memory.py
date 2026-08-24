"""
Memory API Routes
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..core.database import get_db
from ..models.memory import Memory as MemoryModel
from ..schemas.memory import Memory as MemorySchema
from ..schemas.memory import MemoryCreate, MemorySearchResults

router = APIRouter()


def _memory_now() -> datetime:
    return datetime.now(timezone.utc)


@router.post("", response_model=MemorySchema, status_code=201)
async def create_memory(memory: MemoryCreate, db: AsyncSession = Depends(get_db)):
    """Add to memory."""
    now = _memory_now()
    expires_at = now + timedelta(seconds=memory.ttl) if memory.ttl else None
    values = {
        "content": memory.content,
        "type": memory.type or "knowledge",
        "source": memory.source,
        "agent_id": memory.agent_id,
        "metadata_": memory.metadata_ or {},
        "updated_at": now,
        "expires_at": expires_at,
    }

    if settings.DATABASE_URL.startswith("sqlite"):
        upsert = sqlite_insert(MemoryModel).values(
            key=memory.key,
            created_at=now,
            **values,
        )
        upsert = upsert.on_conflict_do_update(
            index_elements=[MemoryModel.key],
            set_=values,
        )
        await db.execute(upsert)
    else:
        from sqlalchemy.dialects.postgresql import insert as pg_insert

        upsert = pg_insert(MemoryModel).values(
            key=memory.key,
            created_at=now,
            **values,
        )
        upsert = upsert.on_conflict_do_update(
            index_elements=[MemoryModel.key],
            set_=values,
        )
        await db.execute(upsert)

    await db.commit()

    result = await db.execute(select(MemoryModel).where(MemoryModel.key == memory.key))
    return result.scalar_one()


@router.get("/search", response_model=MemorySearchResults)
async def search_memory(q: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Search memory."""
    now = _memory_now()
    filters = [
        (MemoryModel.expires_at.is_(None)) | (MemoryModel.expires_at > now),
    ]
    if q:
        filters.append(
            (MemoryModel.key.ilike(f"%{q}%")) | (MemoryModel.content.ilike(f"%{q}%"))
        )

    query = select(MemoryModel).where(*filters).limit(limit)
    result = await db.execute(query)
    results = result.scalars().all()

    count_query = select(func.count()).select_from(MemoryModel).where(*filters)
    total = (await db.execute(count_query)).scalar() or 0

    return MemorySearchResults(results=results, total=total)


@router.get("/{key}", response_model=MemorySchema)
async def get_memory(key: str, db: AsyncSession = Depends(get_db)):
    """Get memory by key."""
    now = _memory_now()
    query = select(MemoryModel).where(
        MemoryModel.key == key,
        (MemoryModel.expires_at.is_(None)) | (MemoryModel.expires_at > now),
    )
    result = await db.execute(query)
    memory = result.scalar_one_or_none()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found or expired")

    # Update access stats
    memory.access_count += 1
    memory.last_accessed_at = now
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
