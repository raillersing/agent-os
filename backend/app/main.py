"""
Agent OS Control Plane — Main Application
"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import agents, auth, control_plane, memory, runs, tools
from .config import settings
from .core.security import require_authenticated_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print(f"Starting Agent OS Control Plane v{settings.VERSION}")
    if len(settings.SECRET_KEY) < 32:
        raise RuntimeError("SECRET_KEY must contain at least 32 characters")
    yield
    # Shutdown
    print("Shutting down Agent OS Control Plane")


app = FastAPI(
    title="Agent OS Control Plane API",
    description="Vendor-neutral orchestration, governance, and observability for AI agents",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
protected = [Depends(require_authenticated_user)]
app.include_router(
    agents.router, prefix="/api/v1/agents", tags=["Agents"], dependencies=protected
)
app.include_router(
    runs.router, prefix="/api/v1/runs", tags=["Runs"], dependencies=protected
)
app.include_router(
    memory.router, prefix="/api/v1/memory", tags=["Memory"], dependencies=protected
)
app.include_router(
    tools.router, prefix="/api/v1/tools", tags=["Tools"], dependencies=protected
)
app.include_router(
    control_plane.router,
    prefix="/api/v1",
    tags=["Control Plane"],
    dependencies=protected,
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.VERSION}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": "Agent OS Control Plane",
        "version": settings.VERSION,
        "docs": "/docs",
    }
