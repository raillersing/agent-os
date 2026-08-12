"""
Test Configuration
"""

import asyncio
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import init_db


def pytest_sessionstart(session):
    """Create the local persistent schema before clients that omit lifespan."""
    asyncio.run(init_db())


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)
