from typing import Any, Dict, List, Optional

from crewai import Agent, Crew, Task
from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent


class CrewAIAgent(BaseAgent):
    """
    The CrewAIAgent is a wrapper around CrewAI's framework,
    allowing for collaborative agent workflows.
    """
    
    def __init__(
        self,
        name: str = "CrewAI",
        description: str = "I coordinate a crew of specialized AI agents to solve complex problems.",
        model_name: str = "gpt-4o",
        temperature: float = 0.5
    ):
        """
        Initialize the CrewAIAgent.
        
        Args:
            name: The name of the agent
            description: A description of what the agent does
            model_name: The name of the LLM model to use
            temperature: The temperature parameter for the LLM
        """
        super().__init__(name, description)
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        # Create the CrewAI agents
        self.researcher = Agent(
            role="Researcher",
            goal="Conduct thorough research on the given topic",
            backstory="You are an expert researcher with a talent for finding and synthesizing information.",
            verbose=True,
            llm=self.llm
        )
        
        self.writer = Agent(
            role="Writer",
            goal="Create well-written, engaging content based on research",
            backstory="You are a skilled writer who can turn complex information into clear, compelling content.",
            verbose=True,
            llm=self.llm
        )
        
        self.critic = Agent(
            role="Critic",
            goal="Evaluate and improve the quality of the content",
            backstory="You are a detail-oriented critic with a keen eye for quality and accuracy.",
            verbose=True,
            llm=self.llm
        )
        
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the CrewAIAgent on the given input.
        
        Args:
            input_text: The input text to process
            **kwargs: Additional keyword arguments
            
        Returns:
            The agent's response as a string
        """
        # Create tasks for the crew
        research_task = Task(
            description=f"Research the following topic thoroughly: {input_text}",
            agent=self.researcher
        )
        
        writing_task = Task(
            description="Create a comprehensive response based on the research",
            agent=self.writer,
            dependencies=[research_task]
        )
        
        critique_task = Task(
            description="Review and improve the written response",
            agent=self.critic,
            dependencies=[writing_task]
        )
        
        # Create the crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.critic],
            tasks=[research_task, writing_task, critique_task],
            verbose=True
        )
        
        # Execute the crew's tasks
        result = crew.kickoff()
        
        return result