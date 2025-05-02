import pytest
from unittest.mock import patch, MagicMock

from agents.base_agent import BaseAgent
from agents.thinker_agent import ThinkerAgent


def test_base_agent():
    agent = BaseAgent()
    with pytest.raises(NotImplementedError):
        agent.run("test input")


@patch("agents.thinker_agent.OpenAI")
def test_thinker_agent(mock_openai):
    # Mock the OpenAI client response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is a thoughtful response"
    mock_client.chat.completions.create.return_value = mock_response
    
    # Create the agent and test it
    agent = ThinkerAgent()
    result = agent.run("What is the meaning of life?")
    
    # Verify the result
    assert result == "This is a thoughtful response"
    
    # Verify that the OpenAI client was called with the correct parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "gpt-4"
    assert len(call_args["messages"]) > 0
    assert "What is the meaning of life?" in str(call_args["messages"])