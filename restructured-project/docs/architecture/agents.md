# Agent Architecture

NeuroNest-AI uses a modular agent architecture that allows for easy extension and customization. This document explains the agent system and how to create new agents.

## Agent Types

NeuroNest-AI supports several types of agents:

### 1. Thinker Agent

The Thinker Agent specializes in analytical thinking and problem-solving. It's designed to:

- Break down complex problems into manageable parts
- Provide step-by-step reasoning
- Analyze situations from multiple perspectives
- Generate creative solutions

### 2. Developer Agent

The Developer Agent specializes in code and technical problem-solving. It can:

- Write and debug code in various programming languages
- Explain technical concepts
- Review and optimize code
- Provide guidance on software architecture and design patterns

### 3. AutoGen Agent

The AutoGen Agent uses the AutoGen framework to coordinate multiple AI agents. It can:

- Orchestrate conversations between specialized agents
- Solve complex problems that require multiple perspectives
- Manage multi-step workflows
- Provide comprehensive solutions by combining different agent capabilities

### 4. CrewAI Agent

The CrewAI Agent uses the CrewAI framework to create and manage a crew of specialized agents. It can:

- Assign roles to different agents based on their capabilities
- Coordinate complex tasks with multiple steps
- Manage dependencies between agent tasks
- Provide a unified interface for interacting with multiple agents

## Agent Implementation

All agents in NeuroNest-AI inherit from the `BaseAgent` class, which defines the common interface and functionality.

### BaseAgent

```python
class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    All agents should inherit from this class and implement the required methods.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize the agent with a name and description.
        """
        self.name = name
        self.description = description
        
    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the agent on the given input.
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }
```

### Creating a New Agent

To create a new agent, you need to:

1. Create a new Python file in the `agents` directory
2. Define a class that inherits from `BaseAgent`
3. Implement the `run` method
4. Register the agent in the database

Here's an example of a simple agent:

```python
from agents.base_agent import BaseAgent
from langchain.llms import OpenAI

class MyCustomAgent(BaseAgent):
    """
    A custom agent that does something specific.
    """
    
    def __init__(self):
        super().__init__(
            name="MyCustom",
            description="A custom agent that does something specific."
        )
        self.llm = OpenAI(temperature=0.7)
    
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the agent on the given input.
        """
        prompt = f"You are a specialized agent that does something specific. Please respond to: {input_text}"
        response = self.llm.generate(prompt)
        return response
```

## Agent Orchestration

The `Orchestrator` class in `core/orchestrator.py` is responsible for managing the flow of messages between agents and coordinating their execution. It:

1. Receives user messages
2. Determines which agent(s) should handle the message
3. Routes the message to the appropriate agent(s)
4. Returns the agent's response

The orchestrator can be extended to implement more sophisticated routing logic, such as:

- Content-based routing (e.g., code questions go to the Developer agent)
- Multi-agent collaboration (e.g., breaking down a complex task for multiple agents)
- Sequential processing (e.g., one agent's output becomes another agent's input)

## Agent Memory

Agents can access conversation history through the `Memory` class in `core/memory.py`. This allows agents to maintain context across multiple interactions and provide more coherent responses.

## Adding a New Agent to the System

To add a new agent to the system:

1. Create the agent class as described above
2. Add the agent to the database by updating the `initialize_agents` function in `main.py`
3. Update the agent registry in the orchestrator

## Testing Agents

Agents can be tested using the pytest framework. See `tests/test_agents.py` for examples of how to test agents.

## Best Practices

When creating new agents:

1. Keep the agent focused on a specific domain or capability
2. Use clear and descriptive names and descriptions
3. Implement proper error handling
4. Document the agent's capabilities and limitations
5. Write tests to verify the agent's behavior
6. Consider the agent's performance and resource requirements