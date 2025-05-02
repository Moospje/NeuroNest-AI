from typing import Any, Dict, List, Optional

import autogen
from autogen import Agent, AssistantAgent, UserProxyAgent, config_list_from_json

from .base_agent import BaseAgent


class AutoGenAgent(BaseAgent):
    """
    The AutoGenAgent is a wrapper around AutoGen's multi-agent framework,
    allowing for complex multi-agent conversations and problem-solving.
    """
    
    def __init__(
        self,
        name: str = "AutoGen",
        description: str = "I coordinate multiple AI agents to solve complex problems.",
        config_list: Optional[List[Dict[str, Any]]] = None,
        llm_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the AutoGenAgent.
        
        Args:
            name: The name of the agent
            description: A description of what the agent does
            config_list: Configuration list for AutoGen
            llm_config: LLM configuration for AutoGen
        """
        super().__init__(name, description)
        
        # Default configuration if none provided
        if config_list is None:
            config_list = [
                {
                    "model": "gpt-4o",
                    "api_key": "YOUR_API_KEY"  # This should be set from environment
                }
            ]
        
        if llm_config is None:
            llm_config = {
                "config_list": config_list,
                "temperature": 0.5
            }
        
        # Create AutoGen agents
        self.assistant = AssistantAgent(
            name="assistant",
            llm_config=llm_config,
            system_message="""You are a helpful AI assistant that can solve complex problems.
            Break down problems step by step and think carefully about the best approach."""
        )
        
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "workspace"}
        )
        
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the AutoGenAgent on the given input.
        
        Args:
            input_text: The input text to process
            **kwargs: Additional keyword arguments
            
        Returns:
            The agent's response as a string
        """
        # Initialize a chat between the user proxy and the assistant
        self.user_proxy.initiate_chat(
            self.assistant,
            message=input_text
        )
        
        # Extract the conversation history
        chat_history = self.user_proxy.chat_messages[self.assistant]
        
        # Format the response
        response = ""
        for message in chat_history[1:]:  # Skip the initial user message
            if message["role"] == "assistant":
                response += message["content"] + "\n\n"
        
        return response.strip()