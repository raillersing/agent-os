"""
Test Configuration
"""

import asyncio
import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("SECRET_KEY", "test-secret-key-with-more-than-32-characters")
os.environ.setdefault("ADMIN_EMAIL", "admin@test.local")
os.environ.setdefault("ADMIN_PASSWORD", "test-password")

from app.main import app
from app.core.database import init_db


def pytest_sessionstart(session):
    """Create the local persistent schema before clients that omit lifespan."""
    asyncio.run(init_db())


@pytest.fixture
def client():
    """Create test client."""
    with TestClient(app) as test_client:
        test_client.headers.update(auth_headers(test_client))
        yield test_client


def auth_headers(test_client: TestClient) -> dict[str, str]:
    response = test_client.post(
        "/api/v1/auth/token",
        json={"email": "admin@test.local", "password": "test-password"},
    )
    response.raise_for_status()
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
