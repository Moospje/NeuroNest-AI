import pytest
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


def test_login(client: TestClient, db: Session):
    """Test login endpoint"""
    # Create a test user
    user = create_test_user(db)
    
    # Test login with correct credentials
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword",
            "device_id": "test-device"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data
    
    # Test login with incorrect password
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword",
            "device_id": "test-device"
        }
    )
    
    assert response.status_code == 401
    
    # Test login with non-existent user
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistentuser",
            "password": "testpassword",
            "device_id": "test-device"
        }
    )
    
    assert response.status_code == 401


def test_refresh_token(client: TestClient, db: Session):
    """Test refresh token endpoint"""
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
    
    # Test refresh token
    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": tokens["refresh_token"],
            "device_id": "test-device"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data
    
    # Test with invalid refresh token
    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid-token",
            "device_id": "test-device"
        }
    )
    
    assert response.status_code == 401


def test_logout(client: TestClient, db: Session):
    """Test logout endpoint"""
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
    
    # Test logout
    response = client.post(
        "/api/v1/auth/logout",
        json={"device_id": "test-device"},
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Successfully logged out"
    
    # Try to use the token after logout
    response = client.post(
        "/api/v1/auth/logout",
        json={"device_id": "test-device"},
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 401