import pytest
from unittest.mock import MagicMock, patch

from core.orchestrator import Orchestrator
from agents.base_agent import BaseAgent


class MockAgent(BaseAgent):
    """Mock agent for testing."""
    
    def __init__(self, name="MockAgent", response="Mock response"):
        super().__init__(name=name, description="Mock agent for testing")
        self.response = response
    
    def run(self, input_text: str, **kwargs) -> str:
        return self.response


def test_orchestrator_initialization():
    """Test orchestrator initialization."""
    # Create mock agents
    agent1 = MockAgent(name="Agent1", response="Response from Agent1")
    agent2 = MockAgent(name="Agent2", response="Response from Agent2")
    
    # Create agent dictionary
    agents = {
        "agent1": agent1,
        "agent2": agent2,
    }
    
    # Initialize orchestrator
    orchestrator = Orchestrator(agents=agents)
    
    # Verify that the agents were stored correctly
    assert orchestrator.agents == agents
    assert orchestrator.get_agent("agent1") == agent1
    assert orchestrator.get_agent("agent2") == agent2
    assert orchestrator.get_agent("nonexistent") is None


def test_process_message_with_specific_agent():
    """Test processing a message with a specific agent."""
    # Create mock agents
    agent1 = MockAgent(name="Agent1", response="Response from Agent1")
    agent2 = MockAgent(name="Agent2", response="Response from Agent2")
    
    # Create agent dictionary
    agents = {
        "agent1": agent1,
        "agent2": agent2,
    }
    
    # Initialize orchestrator
    orchestrator = Orchestrator(agents=agents)
    
    # Process message with specific agent
    result = orchestrator.process_message(
        message="Test message",
        conversation_id="test_conversation",
        user_id="test_user",
        agent_name="agent2"
    )
    
    # Verify the result
    assert result["response"] == "Response from Agent2"
    assert result["agent"] == "agent2"
    assert result["conversation_id"] == "test_conversation"


def test_process_message_with_default_agent():
    """Test processing a message with the default agent."""
    # Create mock agents
    agent1 = MockAgent(name="Agent1", response="Response from Agent1")
    agent2 = MockAgent(name="Agent2", response="Response from Agent2")
    
    # Create agent dictionary
    agents = {
        "agent1": agent1,
        "agent2": agent2,
    }
    
    # Initialize orchestrator
    orchestrator = Orchestrator(agents=agents)
    
    # Process message without specifying an agent
    result = orchestrator.process_message(
        message="Test message",
        conversation_id="test_conversation",
        user_id="test_user"
    )
    
    # Verify the result uses the first agent (default behavior in our implementation)
    assert result["response"] == "Response from Agent1"
    assert result["agent"] == "agent1"
    assert result["conversation_id"] == "test_conversation"


def test_process_message_with_nonexistent_agent():
    """Test processing a message with a nonexistent agent."""
    # Create mock agents
    agent1 = MockAgent(name="Agent1", response="Response from Agent1")
    
    # Create agent dictionary
    agents = {
        "agent1": agent1,
    }
    
    # Initialize orchestrator
    orchestrator = Orchestrator(agents=agents)
    
    # Process message with nonexistent agent
    # Should fall back to the default agent
    result = orchestrator.process_message(
        message="Test message",
        conversation_id="test_conversation",
        user_id="test_user",
        agent_name="nonexistent"
    )
    
    # Verify the result falls back to the first agent
    assert result["response"] == "Response from Agent1"
    assert result["agent"] == "agent1"
    assert result["conversation_id"] == "test_conversation"