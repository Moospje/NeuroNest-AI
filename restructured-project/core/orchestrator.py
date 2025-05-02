from typing import Dict, List, Optional, Union

from agents.base_agent import BaseAgent
from database.models import Conversation, Message


class Orchestrator:
    """
    The Orchestrator is responsible for managing the flow of messages between agents
    and coordinating their execution.
    """
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        """
        Initialize the Orchestrator with a dictionary of agents.
        
        Args:
            agents: A dictionary mapping agent names to agent instances
        """
        self.agents = agents
        
    def process_message(
        self, 
        message: str, 
        conversation_id: str,
        user_id: str,
        agent_name: Optional[str] = None
    ) -> Dict[str, Union[str, List[Dict]]]:
        """
        Process a user message and route it to the appropriate agent(s).
        
        Args:
            message: The user's message
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            agent_name: Optional name of a specific agent to use
            
        Returns:
            A dictionary containing the response and any additional metadata
        """
        # If a specific agent is requested, use that one
        if agent_name and agent_name in self.agents:
            agent = self.agents[agent_name]
            response = agent.run(message)
            return {
                "response": response,
                "agent": agent_name,
                "conversation_id": conversation_id
            }
        
        # Otherwise, determine which agent to use based on the message
        # This is a simple implementation - in a real system, you might use a router agent
        # to determine which agent(s) should handle the message
        
        # For now, just use the first agent
        default_agent_name = list(self.agents.keys())[0]
        agent = self.agents[default_agent_name]
        response = agent.run(message)
        
        return {
            "response": response,
            "agent": default_agent_name,
            "conversation_id": conversation_id
        }
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.
        
        Args:
            agent_name: The name of the agent
            
        Returns:
            The agent instance, or None if not found
        """
        return self.agents.get(agent_name)