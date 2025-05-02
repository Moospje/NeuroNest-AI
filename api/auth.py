from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.settings import settings
from core.security import verify_password
from database import models
from database.session import get_db

# Redis client for token storage
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    device_id: Optional[str] = None


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_tokens(user_id: UUID, device_id: str):
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": str(user_id), "device_id": device_id}
    access_token = jwt.encode(
        {**access_token_data, "exp": datetime.utcnow() + access_token_expires},
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    
    # Create refresh token (longer expiry)
    refresh_token_expires = timedelta(days=30)
    refresh_token = jwt.encode(
        {**access_token_data, "exp": datetime.utcnow() + refresh_token_expires},
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    
    # Store tokens in Redis with device_id
    token_key = f"user:{user_id}:device:{device_id}"
    redis_client.hset(token_key, mapping={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "created_at": datetime.utcnow().isoformat(),
    })
    redis_client.expire(token_key, int(refresh_token_expires.total_seconds()))
    
    return access_token, refresh_token


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        device_id: str = payload.get("device_id")
        if user_id is None or device_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id, device_id=device_id)
    except JWTError:
        raise credentials_exception
    
    # Verify token exists in Redis for this device
    token_key = f"user:{token_data.sub}:device:{token_data.device_id}"
    stored_token = redis_client.hget(token_key, "access_token")
    if not stored_token or stored_token != token:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def revoke_tokens(user_id: UUID, device_id: str):
    """Revoke tokens for a specific device"""
    token_key = f"user:{user_id}:device:{device_id}"
    redis_client.delete(token_key)


def revoke_all_tokens(user_id: UUID):
    """Revoke all tokens for a user (all devices)"""
    pattern = f"user:{user_id}:device:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)