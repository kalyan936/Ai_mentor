"""
AI Mentor - Basic API Tests.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Set environment variables for testing before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test_ai_mentor.db"
os.environ["LLM_PROVIDER"] = "mock"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.main import app
from app.db.database import Base, engine

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    # Drop and recreate tables before running logic
    Base.metadata.drop_all(bind=engine)
    # The lifespan context manager will call init_db and create_all
    yield 
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_api_health(client):
    """Test API health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_register_user(client):
    """Test user registration."""
    response = client.post("/api/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "learning_level": "beginner",
        "daily_study_time": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["id"] > 0


def test_login_user(client):
    """Test user login."""
    # Register first
    client.post("/api/users/register", json={
        "name": "Login Test",
        "email": "login@test.com"
    })

    # Login
    response = client.post("/api/users/login", json={
        "email": "login@test.com"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "login@test.com"


def test_get_curriculum(client):
    """Test curriculum endpoint."""
    response = client.get("/api/roadmap/curriculum/all")
    assert response.status_code == 200
    data = response.json()
    assert "python" in data
    assert "mysql" in data
    assert "ml" in data


def test_onboard_user(client):
    """Test user onboarding."""
    # Register user
    reg = client.post("/api/users/register", json={
        "name": "Onboard User",
        "email": "onboard@test.com"
    })
    user_id = reg.json()["id"]

    response = client.post("/api/users/onboard", json={
        "user_id": user_id,
        "selected_topics": ["python", "ml"],
        "current_level": "beginner",
        "goals": "Become a data scientist",
        "daily_study_time": 60,
        "preferred_style": "hands-on"
    })
    assert response.status_code == 200
    assert response.json()["selected_topics"] == ["python", "ml"]


def test_dashboard(client):
    """Test dashboard endpoint."""
    # Register user
    reg = client.post("/api/users/register", json={
        "name": "Dashboard User",
        "email": "dashboard@test.com"
    })
    user_id = reg.json()["id"]

    response = client.get(f"/api/progress/dashboard/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "user_name" in data
    assert "streak_days" in data
    assert "topics_mastery" in data


def test_progress_update(client):
    """Test progress update."""
    reg = client.post("/api/users/register", json={
        "name": "Progress User",
        "email": "progress@test.com"
    })
    user_id = reg.json()["id"]

    response = client.post("/api/progress/update", json={
        "user_id": user_id,
        "topic": "python",
        "subtopic": "functions",
        "status": "in_progress",
        "score": 75.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "python"
    assert data["subtopic"] == "functions"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
