"""
Agent OS Control Plane — Main Application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api import agents, runs, memory, auth, tools


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"Starting Agent OS Control Plane v{settings.VERSION}")
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
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(runs.router, prefix="/api/v1/runs", tags=["Runs"])
app.include_router(memory.router, prefix="/api/v1/memory", tags=["Memory"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["Tools"])


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
