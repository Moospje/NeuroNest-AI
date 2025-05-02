from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agents import AutoGenAgent, CrewAIAgent, DeveloperAgent, ThinkerAgent
from database.models import Agent, User
from database.session import get_db

from .auth import get_current_user

router = APIRouter()


class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    agent_type: str


@router.get("/", response_model=List[AgentResponse])
def get_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get all available agents.
    """
    agents = db.query(Agent).filter(Agent.is_active == True).all()
    
    return [
        {
            "id": str(agent.id),
            "name": agent.name,
            "description": agent.description,
            "agent_type": agent.agent_type
        }
        for agent in agents
    ]


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific agent by ID.
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    
    return {
        "id": str(agent.id),
        "name": agent.name,
        "description": agent.description,
        "agent_type": agent.agent_type
    }


@router.get("/types", response_model=List[str])
def get_agent_types(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get all available agent types.
    """
    return [
        "ThinkerAgent",
        "DeveloperAgent",
        "AutoGenAgent",
        "CrewAIAgent"
    ]