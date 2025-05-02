from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database.session import get_db
from database import models

router = APIRouter()


@router.get("/")
async def list_agents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    List available agents
    """
    # This is a placeholder implementation
    # In a real implementation, we would return the list of agents
    return [
        {
            "id": "placeholder_id_1",
            "name": "GPT-4 Agent",
            "description": "General purpose GPT-4 agent",
            "type": "openai"
        },
        {
            "id": "placeholder_id_2",
            "name": "Developer Agent",
            "description": "Specialized agent for development tasks",
            "type": "openai"
        }
    ]