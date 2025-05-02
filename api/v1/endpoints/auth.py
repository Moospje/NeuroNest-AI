from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from api.auth import (
    Token, authenticate_user, create_tokens, get_current_active_user,
    revoke_tokens, revoke_all_tokens
)
from core.security import create_access_token, verify_password
from database.session import get_db
from database import models

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    device_id: str = Body(..., embed=True)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create device record if it doesn't exist
    device = db.query(models.Device).filter(
        models.Device.user_id == user.id,
        models.Device.name == device_id
    ).first()
    
    if not device:
        device = models.Device(
            user_id=user.id,
            name=device_id,
            device_token=device_id  # In a real app, generate a unique token
        )
        db.add(device)
        db.commit()
        db.refresh(device)
    
    # Create tokens
    access_token, refresh_token = create_tokens(user.id, device_id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    db: Session = Depends(get_db),
    refresh_token: str = Body(..., embed=True),
    device_id: str = Body(..., embed=True)
):
    """
    Refresh access token using refresh token
    """
    try:
        # Validate refresh token
        from jose import jwt
        from config.settings import settings
        
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        token_device_id = payload.get("device_id")
        
        if not user_id or token_device_id != device_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        # Create new tokens
        access_token, refresh_token = create_tokens(user.id, device_id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate refresh token: {str(e)}",
        )


@router.post("/logout")
async def logout(
    current_user = Depends(get_current_active_user),
    device_id: str = Body(..., embed=True)
):
    """
    Logout from current device
    """
    revoke_tokens(current_user.id, device_id)
    return {"message": "Successfully logged out"}


@router.post("/logout-all")
async def logout_all(current_user = Depends(get_current_active_user)):
    """
    Logout from all devices
    """
    revoke_all_tokens(current_user.id)
    return {"message": "Successfully logged out from all devices"}