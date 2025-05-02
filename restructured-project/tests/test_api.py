from fastapi.testclient import TestClient

from database.models import User
from core.security import get_password_hash


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to NeuroNest-AI API" in response.json()["message"]


def test_register_user(client, db):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    
    # Check that the user was created in the database
    user = db.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    assert user.username == "testuser"


def test_login(client, db):
    # Create a user
    hashed_password = get_password_hash("password123")
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    
    # Try to login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"