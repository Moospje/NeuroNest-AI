from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    All agents should inherit from this class and implement the required methods.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize the agent with a name and description.
        
        Args:
            name: The name of the agent
            description: A description of what the agent does
        """
        self.name = name
        self.description = description
        
    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the agent on the given input.
        
        Args:
            input_text: The input text to process
            **kwargs: Additional keyword arguments
            
        Returns:
            The agent's response as a string
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.
        
        Returns:
            A dictionary containing agent information
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }