"""Tests for main application."""

import pytest
from fastapi.testclient import TestClient

from {{PROJECT_SLUG}}.main import create_application


@pytest.fixture
def client():
    """Create test client."""
    app = create_application()
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "guardian_framework" in data


def test_health_endpoint(client):
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"