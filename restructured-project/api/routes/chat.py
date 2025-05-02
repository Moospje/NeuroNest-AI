import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from agents import DeveloperAgent, ThinkerAgent
from core.memory import Memory
from core.orchestrator import Orchestrator
from database.models import Conversation, Message, User
from database.session import get_db

from .auth import get_current_user

router = APIRouter()

# Initialize agents
thinker_agent = ThinkerAgent()
developer_agent = DeveloperAgent()

# Initialize orchestrator with agents
orchestrator = Orchestrator({
    "thinker": thinker_agent,
    "developer": developer_agent,
})


class MessageCreate(BaseModel):
    content: str
    agent_name: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    content: str
    role: str
    agent_id: Optional[str] = None
    created_at: str


class ConversationCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ConversationResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    created_at: str
    messages: List[MessageResponse] = []


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new conversation.
    """
    conversation = Conversation(
        user_id=current_user.id,
        title=conversation_data.title,
        description=conversation_data.description,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "description": conversation.description,
        "created_at": conversation.created_at.isoformat(),
        "messages": []
    }


@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
) -> Any:
    """
    Get all conversations for the current user.
    """
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    result = []
    for conv in conversations:
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.created_at)
            .all()
        )
        
        message_responses = []
        for msg in messages:
            message_responses.append({
                "id": str(msg.id),
                "content": msg.content,
                "role": msg.role,
                "agent_id": str(msg.agent_id) if msg.agent_id else None,
                "created_at": msg.created_at.isoformat()
            })
        
        result.append({
            "id": str(conv.id),
            "title": conv.title,
            "description": conv.description,
            "created_at": conv.created_at.isoformat(),
            "messages": message_responses
        })
    
    return result


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific conversation by ID.
    """
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    # Get messages for this conversation
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .all()
    )
    
    message_responses = []
    for msg in messages:
        message_responses.append({
            "id": str(msg.id),
            "content": msg.content,
            "role": msg.role,
            "agent_id": str(msg.agent_id) if msg.agent_id else None,
            "created_at": msg.created_at.isoformat()
        })
    
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "description": conversation.description,
        "created_at": conversation.created_at.isoformat(),
        "messages": message_responses
    }


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def create_message(
    conversation_id: str,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new message in a conversation and get a response from the agent.
    """
    # Check if conversation exists and belongs to the user
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    # Initialize memory
    memory = Memory(db)
    
    # Save user message
    user_message = memory.add_message(
        conversation_id=conversation_id,
        content=message_data.content,
        role="user"
    )
    
    # Process message with orchestrator
    response_data = orchestrator.process_message(
        message=message_data.content,
        conversation_id=conversation_id,
        user_id=str(current_user.id),
        agent_name=message_data.agent_name
    )
    
    # Get agent ID
    agent_name = response_data.get("agent")
    agent = None
    if agent_name:
        agent = (
            db.query(Agent)
            .filter(Agent.name == agent_name)
            .first()
        )
    
    # Save assistant message
    assistant_message = memory.add_message(
        conversation_id=conversation_id,
        content=response_data.get("response"),
        role="assistant",
        agent_id=agent.id if agent else None
    )
    
    return {
        "id": str(assistant_message.id),
        "content": assistant_message.content,
        "role": assistant_message.role,
        "agent_id": str(assistant_message.agent_id) if assistant_message.agent_id else None,
        "created_at": assistant_message.created_at.isoformat()
    }