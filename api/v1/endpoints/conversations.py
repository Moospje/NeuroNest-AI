from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database.session import get_db
from database import models

router = APIRouter()


@router.get("/")
async def list_conversations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    List user conversations
    """
    # This is a placeholder implementation
    # In a real implementation, we would return the list of conversations
    return [
        {
            "id": "placeholder_id_1",
            "title": "Project Planning",
            "created_at": "2025-05-01T12:00:00Z",
            "updated_at": "2025-05-01T12:30:00Z"
        },
        {
            "id": "placeholder_id_2",
            "title": "Code Review",
            "created_at": "2025-05-02T10:00:00Z",
            "updated_at": "2025-05-02T10:45:00Z"
        }
    ]