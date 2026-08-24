"""
Test Configuration
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Make repo-root imports such as `scripts.evals` available to tests.
_REPO_ROOT = str(Path(__file__).resolve().parents[2])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# Use an isolated on-disk SQLite database for every test session so that state
# never leaks between runs and tests remain hermetic.
_TEST_DB_DIR = tempfile.mkdtemp(prefix="agent_os_test_")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{_TEST_DB_DIR}/test.db"
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("SECRET_KEY", "test-secret-key-with-more-than-32-characters")
os.environ.setdefault("ADMIN_EMAIL", "admin@test.local")
os.environ.setdefault("ADMIN_PASSWORD", "test-password")

import pytest
from fastapi.testclient import TestClient

from app.main import app


def pytest_sessionstart(session):
    """Create the local persistent schema by running the latest Alembic revision."""
    env = os.environ.copy()
    env["DATABASE_URL"] = TEST_DATABASE_URL
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(Path(__file__).resolve().parent.parent),
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Alembic upgrade failed for test database:\n{result.stdout}\n{result.stderr}"
        )


def pytest_sessionfinish(session, exitstatus):
    """Remove the temporary test database."""
    shutil.rmtree(_TEST_DB_DIR, ignore_errors=True)


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
