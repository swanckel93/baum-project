import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "StudioHub API - Design Studio Orchestration Platform"
    assert data["version"] == "1.0.0"
    assert data["environment"] == "development"


def test_simple_health_check(client):
    """Test the simple health check endpoint."""
    response = client.get("/api/v1/health/simple")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "StudioHub API is running"


def test_detailed_health_check(client):
    """Test the detailed health check endpoint."""
    response = client.get("/api/v1/health")
    # Health check might return 503 if Redis is not available, which is expected in tests
    assert response.status_code in [200, 503]
    data = response.json() if response.status_code == 200 else response.json()["detail"]
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert data["version"] == "1.0.0"
    assert "services" in data
    assert "application" in data["services"]
    assert data["services"]["application"] == "healthy"


def test_docs_available_in_development(client):
    """Test that API docs are available in development environment."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()


def test_redoc_available_in_development(client):
    """Test that ReDoc is available in development environment."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower() or "redocly" in response.text.lower()
