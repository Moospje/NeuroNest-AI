from typing import Any, Dict, List, Optional

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .base_agent import BaseAgent


class ThinkerAgent(BaseAgent):
    """
    The ThinkerAgent is responsible for analyzing problems, breaking them down,
    and providing thoughtful responses.
    """
    
    def __init__(
        self,
        name: str = "Thinker",
        description: str = "I analyze problems and think through solutions step by step.",
        model_name: str = "gpt-4o",
        temperature: float = 0.7
    ):
        """
        Initialize the ThinkerAgent.
        
        Args:
            name: The name of the agent
            description: A description of what the agent does
            model_name: The name of the LLM model to use
            temperature: The temperature parameter for the LLM
        """
        super().__init__(name, description)
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a thoughtful assistant that carefully analyzes problems and thinks through solutions step by step.
            
When presented with a problem or question:
1. Break down the problem into its core components
2. Consider multiple approaches or perspectives
3. Evaluate the pros and cons of each approach
4. Provide a well-reasoned conclusion or recommendation
            
Always show your reasoning process clearly."""),
            ("human", "{input}")
        ])
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the ThinkerAgent on the given input.
        
        Args:
            input_text: The input text to process
            **kwargs: Additional keyword arguments
            
        Returns:
            The agent's response as a string
        """
        response = self.chain.run(input=input_text)
        return response