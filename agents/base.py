from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
    
    @abstractmethod
    async def process(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a list of messages and return a response."""
        pass
    
    @abstractmethod
    async def stream_process(self, messages: List[Dict[str, Any]]):
        """Process a list of messages and stream the response."""
        pass