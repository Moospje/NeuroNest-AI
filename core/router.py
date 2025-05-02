from typing import Dict, List, Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.agents import AgentManager
from database import models


class MessageRouter:
    """Routes messages to the appropriate agent."""
    
    def __init__(self, db: Session):
        self.db = db
        self.agent_manager = AgentManager(db)
    
    async def route_message(self, conversation_id: UUID, content: str, 
                           agent_id: Optional[UUID] = None) -> Dict[str, Any]:
        """
        Route a message to the appropriate agent and store the response.
        
        Args:
            conversation_id: The ID of the conversation
            content: The message content
            agent_id: Optional agent ID to route to. If None, will use the last agent
                     used in the conversation or a default agent.
        
        Returns:
            The agent's response
        """
        # Get conversation
        conversation = self.db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError(f"Conversation not found: {conversation_id}")
        
        # If no agent_id provided, try to find the last agent used in this conversation
        if not agent_id:
            last_agent_message = self.db.query(models.Message).filter(
                models.Message.conversation_id == conversation_id,
                models.Message.agent_id.isnot(None)
            ).order_by(models.Message.created_at.desc()).first()
            
            if last_agent_message:
                agent_id = last_agent_message.agent_id
            else:
                # Get default agent (first one in the database)
                default_agent = self.db.query(models.Agent).first()
                if not default_agent:
                    raise ValueError("No agents available")
                agent_id = default_agent.id
        
        # Store user message
        user_message = models.Message(
            conversation_id=conversation_id,
            content=content,
            role="user"
        )
        self.db.add(user_message)
        self.db.commit()
        self.db.refresh(user_message)
        
        # Get agent
        agent = self.agent_manager.get_agent(agent_id)
        
        # Get conversation history
        messages = self.db.query(models.Message).filter(
            models.Message.conversation_id == conversation_id
        ).order_by(models.Message.created_at).all()
        
        # Format messages for agent
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Process message with agent
        response = await agent.process(formatted_messages)
        
        # Store agent response
        agent_message = models.Message(
            conversation_id=conversation_id,
            agent_id=agent_id,
            content=response["content"],
            role="assistant"
        )
        self.db.add(agent_message)
        self.db.commit()
        self.db.refresh(agent_message)
        
        return response
    
    async def stream_message(self, conversation_id: UUID, content: str,
                            agent_id: Optional[UUID] = None):
        """
        Stream a message to the appropriate agent.
        
        Args:
            conversation_id: The ID of the conversation
            content: The message content
            agent_id: Optional agent ID to route to. If None, will use the last agent
                     used in the conversation or a default agent.
        
        Yields:
            Chunks of the agent's response
        """
        # Get conversation
        conversation = self.db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError(f"Conversation not found: {conversation_id}")
        
        # If no agent_id provided, try to find the last agent used in this conversation
        if not agent_id:
            last_agent_message = self.db.query(models.Message).filter(
                models.Message.conversation_id == conversation_id,
                models.Message.agent_id.isnot(None)
            ).order_by(models.Message.created_at.desc()).first()
            
            if last_agent_message:
                agent_id = last_agent_message.agent_id
            else:
                # Get default agent (first one in the database)
                default_agent = self.db.query(models.Agent).first()
                if not default_agent:
                    raise ValueError("No agents available")
                agent_id = default_agent.id
        
        # Store user message
        user_message = models.Message(
            conversation_id=conversation_id,
            content=content,
            role="user"
        )
        self.db.add(user_message)
        self.db.commit()
        self.db.refresh(user_message)
        
        # Get agent
        agent = self.agent_manager.get_agent(agent_id)
        
        # Get conversation history
        messages = self.db.query(models.Message).filter(
            models.Message.conversation_id == conversation_id
        ).order_by(models.Message.created_at).all()
        
        # Format messages for agent
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Process message with agent and collect the full response
        full_response = ""
        async for chunk in agent.stream_process(formatted_messages):
            full_response += chunk
            yield chunk
        
        # Store agent response
        agent_message = models.Message(
            conversation_id=conversation_id,
            agent_id=agent_id,
            content=full_response,
            role="assistant"
        )
        self.db.add(agent_message)
        self.db.commit()