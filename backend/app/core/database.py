"""
Database Configuration
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from ..config import settings

# Create async engine
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine_options = {"echo": settings.DATABASE_ECHO, "pool_pre_ping": True}
if not database_url.startswith("sqlite"):
    engine_options.update({"pool_size": 20, "max_overflow": 0})
engine = create_async_engine(database_url, **engine_options)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()


async def get_db():
    """Dependency for getting async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
