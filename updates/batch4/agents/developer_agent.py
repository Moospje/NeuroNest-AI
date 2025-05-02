from typing import Any, Dict, List, Optional

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .base_agent import BaseAgent


class DeveloperAgent(BaseAgent):
    """
    The DeveloperAgent is responsible for writing and reviewing code,
    explaining technical concepts, and providing development guidance.
    """
    
    def __init__(
        self,
        name: str = "Developer",
        description: str = "I write code, review code, and provide technical guidance.",
        model_name: str = "gpt-4o",
        temperature: float = 0.2
    ):
        """
        Initialize the DeveloperAgent.
        
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
            ("system", """You are an expert software developer assistant that helps with coding tasks, code reviews, and technical guidance.

When presented with a coding task or technical question:
1. Understand the requirements or problem thoroughly
2. Provide clean, efficient, and well-documented code solutions
3. Explain your approach and any important considerations
4. Follow best practices for the relevant programming language or framework

For code reviews:
1. Identify potential bugs, performance issues, or security vulnerabilities
2. Suggest improvements for readability and maintainability
3. Highlight good practices already present in the code

Always prioritize writing production-quality code that is secure, efficient, and maintainable."""),
            ("human", "{input}")
        ])
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the DeveloperAgent on the given input.
        
        Args:
            input_text: The input text to process
            **kwargs: Additional keyword arguments
            
        Returns:
            The agent's response as a string
        """
        response = self.chain.run(input=input_text)
        return response