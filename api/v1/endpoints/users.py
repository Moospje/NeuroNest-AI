from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database.session import get_db
from database import models

router = APIRouter()


@router.get("/me")
async def read_users_me(
    current_user: models.User = Depends(get_current_user)
):
    """
    Get current user
    """
    # This is a placeholder implementation
    # In a real implementation, we would return the current user
    return {
        "id": "placeholder_id",
        "email": "user@example.com",
        "username": "example_user"
    }