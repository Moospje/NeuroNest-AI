import pytest
from datetime import datetime, timedelta
from jose import jwt

from core.security import create_access_token, verify_password, get_password_hash
from config.settings import settings


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Verify that the hash is different from the original password
    assert hashed_password != password
    
    # Verify that the password verification works
    assert verify_password(password, hashed_password)
    
    # Verify that incorrect password fails
    assert not verify_password("wrongpassword", hashed_password)


def test_create_access_token():
    """Test JWT token creation."""
    # Create a token with a specific subject
    subject = "testuser"
    token = create_access_token(subject=subject)
    
    # Decode the token
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    
    # Verify the subject
    assert payload["sub"] == subject
    
    # Verify that the token has an expiration time
    assert "exp" in payload


def test_token_expiration():
    """Test token expiration."""
    # Create a token with a short expiration time
    subject = "testuser"
    expires_delta = timedelta(minutes=1)
    token = create_access_token(subject=subject, expires_delta=expires_delta)
    
    # Decode the token
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    
    # Verify that the expiration time is approximately 1 minute in the future
    exp_time = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    time_diff = exp_time - now
    
    # Allow for a small margin of error (a few seconds)
    assert timedelta(seconds=50) < time_diff < timedelta(seconds=70)