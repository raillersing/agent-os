"""
API Tests
"""

from fastapi.testclient import TestClient

from app.main import app

from .conftest import auth_headers

client = TestClient(app)
client.headers.update(auth_headers(client))


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_protected_api_rejects_anonymous_request():
    anonymous = TestClient(app)
    response = anonymous.get("/api/v1/workspaces")
    assert response.status_code == 401


def test_token_endpoint_accepts_configured_admin():
    anonymous = TestClient(app)
    response = anonymous.post(
        "/api/v1/auth/token",
        json={"email": "admin@test.local", "password": "test-password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Agent OS Control Plane"


def test_create_agent():
    """Test agent creation."""
    response = client.post(
        "/api/v1/agents",
        json={
            "name": "test-agent",
            "model": "gpt-4",
            "capabilities": ["text-generation"],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test-agent"
    assert data["model"] == "gpt-4"
    assert data["status"] == "active"
    assert "id" in data


def test_list_agents():
    """Test agent listing."""
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_agent():
    """Test get agent by ID."""
    # First create an agent
    create_response = client.post(
        "/api/v1/agents",
        json={"name": "test-agent", "model": "gpt-4"},
    )
    agent_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/v1/agents/{agent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == agent_id


def test_list_tools():
    """Test tool listing."""
    response = client.get("/api/v1/tools")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
