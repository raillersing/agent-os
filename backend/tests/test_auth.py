"""Authentication endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_token_returns_cookie_and_bearer_token():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/token",
            json={"email": "admin@test.local", "password": "test-password"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["access_token"]
        assert "access_token" in response.cookies
        assert response.cookies["access_token"]


def test_token_invalid_credentials():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/token",
            json={"email": "admin@test.local", "password": "wrong-password"},
        )
        assert response.status_code == 401


def test_logout_clears_cookie():
    with TestClient(app) as client:
        login = client.post(
            "/api/v1/auth/token",
            json={"email": "admin@test.local", "password": "test-password"},
        )
        assert login.status_code == 200
        assert "access_token" in client.cookies

        logout = client.post("/api/v1/auth/logout")
        assert logout.status_code == 200
        cookie = logout.headers.get("set-cookie", "")
        assert "access_token=" in cookie
        assert "Max-Age=0" in cookie or "expires=" in cookie.lower()


def test_protected_route_requires_auth():
    with TestClient(app) as client:
        response = client.get("/api/v1/agents")
        assert response.status_code == 401


def test_protected_route_accepts_cookie_auth():
    with TestClient(app) as client:
        login = client.post(
            "/api/v1/auth/token",
            json={"email": "admin@test.local", "password": "test-password"},
        )
        assert login.status_code == 200

        response = client.get("/api/v1/agents")
        assert response.status_code == 200
