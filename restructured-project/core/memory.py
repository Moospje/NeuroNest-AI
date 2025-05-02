import json
from typing import Dict, List, Optional, Union

import redis
from sqlalchemy.orm import Session

from config.settings import settings
from database.models import Conversation, Message


class Memory:
    """
    The Memory class is responsible for storing and retrieving conversation history.
    It uses both Redis for fast access to recent conversations and PostgreSQL for
    persistent storage.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the Memory with database session and Redis connection.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        
    def add_message(
        self,
        conversation_id: str,
        content: str,
        role: str,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Message:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            content: The message content
            role: The role of the message sender ('user', 'assistant', 'system')
            agent_id: Optional ID of the agent that generated the message
            metadata: Optional metadata for the message
            
        Returns:
            The created Message object
        """
        # Create the message in the database
        message = Message(
            conversation_id=conversation_id,
            content=content,
            role=role,
            agent_id=agent_id,
            metadata=metadata or {}
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        # Also store in Redis for quick access
        redis_key = f"conversation:{conversation_id}:messages"
        message_data = {
            "id": str(message.id),
            "content": content,
            "role": role,
            "agent_id": str(agent_id) if agent_id else None,
            "created_at": message.created_at.isoformat()
        }
        self.redis.rpush(redis_key, json.dumps(message_data))
        # Set expiration for Redis key (e.g., 1 day)
        self.redis.expire(redis_key, 86400)
        
        return message
    
    def get_conversation_history(
        self, 
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get the history of a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of messages in the conversation
        """
        # Try to get from Redis first
        redis_key = f"conversation:{conversation_id}:messages"
        redis_messages = self.redis.lrange(redis_key, 0, limit - 1)
        
        if redis_messages:
            return [json.loads(msg) for msg in redis_messages]
        
        # If not in Redis, get from database
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .limit(limit)
            .all()
        )
        
        # Format messages
        result = []
        for msg in messages:
            message_data = {
                "id": str(msg.id),
                "content": msg.content,
                "role": msg.role,
                "agent_id": str(msg.agent_id) if msg.agent_id else None,
                "created_at": msg.created_at.isoformat()
            }
            result.append(message_data)
            
            # Also store in Redis for future quick access
            self.redis.rpush(redis_key, json.dumps(message_data))
        
        # Set expiration for Redis key (e.g., 1 day)
        if result:
            self.redis.expire(redis_key, 86400)
            
        return result