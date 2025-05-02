from typing import Dict, List, Optional, Type, Any
from uuid import UUID

from sqlalchemy.orm import Session

from agents.base import BaseAgent
from agents.openai_agent import OpenAIAgent
from database import models


class AgentRegistry:
    """Registry for all agent types in the system."""
    
    _registry: Dict[str, Type[BaseAgent]] = {
        "openai": OpenAIAgent,
    }
    
    @classmethod
    def register(cls, agent_type: str, agent_class: Type[BaseAgent]):
        """Register a new agent type."""
        cls._registry[agent_type] = agent_class
    
    @classmethod
    def get_agent_class(cls, agent_type: str) -> Type[BaseAgent]:
        """Get the agent class for a given type."""
        if agent_type not in cls._registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls._registry[agent_type]
    
    @classmethod
    def create_agent(cls, agent_type: str, name: str, config: Optional[Dict[str, Any]] = None) -> BaseAgent:
        """Create a new agent instance."""
        agent_class = cls.get_agent_class(agent_type)
        return agent_class(name=name, config=config)


class AgentManager:
    """Manager for agent instances."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_agent(self, agent_id: UUID) -> BaseAgent:
        """Get an agent instance by ID."""
        agent_record = self.db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if not agent_record:
            raise ValueError(f"Agent not found: {agent_id}")
        
        # Parse config if it exists
        config = None
        if agent_record.config:
            import json
            try:
                config = json.loads(agent_record.config)
            except json.JSONDecodeError:
                pass
        
        return AgentRegistry.create_agent(
            agent_type=agent_record.type,
            name=agent_record.name,
            config=config
        )
    
    def list_agents(self) -> List[models.Agent]:
        """List all available agents."""
        return self.db.query(models.Agent).all()
    
    def create_agent(self, name: str, agent_type: str, description: Optional[str] = None, 
                    config: Optional[Dict[str, Any]] = None) -> models.Agent:
        """Create a new agent in the database."""
        # Validate agent type
        AgentRegistry.get_agent_class(agent_type)
        
        # Serialize config if provided
        config_str = None
        if config:
            import json
            config_str = json.dumps(config)
        
        # Create agent record
        agent = models.Agent(
            name=name,
            type=agent_type,
            description=description,
            config=config_str
        )
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        
        return agent
    
    def update_agent(self, agent_id: UUID, **kwargs) -> models.Agent:
        """Update an agent in the database."""
        agent = self.db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        
        # Update fields
        for key, value in kwargs.items():
            if key == 'config' and isinstance(value, dict):
                import json
                value = json.dumps(value)
            setattr(agent, key, value)
        
        self.db.commit()
        self.db.refresh(agent)
        
        return agent
    
    def delete_agent(self, agent_id: UUID) -> bool:
        """Delete an agent from the database."""
        agent = self.db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if not agent:
            return False
        
        self.db.delete(agent)
        self.db.commit()
        
        return True