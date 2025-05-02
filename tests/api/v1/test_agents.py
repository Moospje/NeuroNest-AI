import pytest
import json
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from core.security import get_password_hash
from database import models


def create_test_user(db: Session):
    """Create a test user in the database"""
    user = models.User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_agent(db: Session):
    """Create a test agent in the database"""
    agent = models.Agent(
        name="Test Agent",
        type="openai",
        description="A test agent",
        config=json.dumps({"model": "gpt-3.5-turbo"})
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


def get_auth_headers(client: TestClient, db: Session):
    """Get authentication headers for API requests"""
    # Create a test user
    user = create_test_user(db)
    
    # Login to get tokens
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword",
            "device_id": "test-device"
        }
    )
    
    tokens = login_response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_create_agent(client: TestClient, db: Session):
    """Test creating a new agent"""
    headers = get_auth_headers(client, db)
    
    # Test creating a new agent
    response = client.post(
        "/api/v1/agents",
        json={
            "name": "New Agent",
            "type": "openai",
            "description": "A new test agent",
            "config": {"model": "gpt-4"}
        },
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Agent"
    assert data["type"] == "openai"
    assert data["description"] == "A new test agent"
    assert "id" in data
    
    # Verify the agent was created in the database
    agent = db.query(models.Agent).filter(models.Agent.name == "New Agent").first()
    assert agent is not None
    assert agent.type == "openai"
    
    # Test creating an agent with invalid type
    response = client.post(
        "/api/v1/agents",
        json={
            "name": "Invalid Agent",
            "type": "invalid_type",
            "description": "An agent with invalid type"
        },
        headers=headers
    )
    
    assert response.status_code == 400


def test_get_agents(client: TestClient, db: Session):
    """Test getting all agents"""
    headers = get_auth_headers(client, db)
    
    # Create some test agents
    agent1 = create_test_agent(db)
    agent2 = models.Agent(
        name="Another Agent",
        type="openai",
        description="Another test agent"
    )
    db.add(agent2)
    db.commit()
    
    # Test getting all agents
    response = client.get("/api/v1/agents", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Agent"
    assert data[1]["name"] == "Another Agent"


def test_get_agent(client: TestClient, db: Session):
    """Test getting a specific agent"""
    headers = get_auth_headers(client, db)
    
    # Create a test agent
    agent = create_test_agent(db)
    
    # Test getting the agent
    response = client.get(f"/api/v1/agents/{agent.id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Agent"
    assert data["type"] == "openai"
    assert data["description"] == "A test agent"
    assert data["id"] == str(agent.id)
    
    # Test getting a non-existent agent
    response = client.get("/api/v1/agents/00000000-0000-0000-0000-000000000000", headers=headers)
    
    assert response.status_code == 404


def test_update_agent(client: TestClient, db: Session):
    """Test updating an agent"""
    headers = get_auth_headers(client, db)
    
    # Create a test agent
    agent = create_test_agent(db)
    
    # Test updating the agent
    response = client.put(
        f"/api/v1/agents/{agent.id}",
        json={
            "name": "Updated Agent",
            "description": "An updated test agent",
            "config": {"model": "gpt-4-turbo"}
        },
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Agent"
    assert data["description"] == "An updated test agent"
    
    # Verify the agent was updated in the database
    updated_agent = db.query(models.Agent).filter(models.Agent.id == agent.id).first()
    assert updated_agent.name == "Updated Agent"
    assert updated_agent.description == "An updated test agent"
    
    # Test updating a non-existent agent
    response = client.put(
        "/api/v1/agents/00000000-0000-0000-0000-000000000000",
        json={"name": "Non-existent Agent"},
        headers=headers
    )
    
    assert response.status_code == 404


def test_delete_agent(client: TestClient, db: Session):
    """Test deleting an agent"""
    headers = get_auth_headers(client, db)
    
    # Create a test agent
    agent = create_test_agent(db)
    
    # Test deleting the agent
    response = client.delete(f"/api/v1/agents/{agent.id}", headers=headers)
    
    assert response.status_code == 200
    
    # Verify the agent was deleted from the database
    deleted_agent = db.query(models.Agent).filter(models.Agent.id == agent.id).first()
    assert deleted_agent is None
    
    # Test deleting a non-existent agent
    response = client.delete("/api/v1/agents/00000000-0000-0000-0000-000000000000", headers=headers)
    
    assert response.status_code == 404