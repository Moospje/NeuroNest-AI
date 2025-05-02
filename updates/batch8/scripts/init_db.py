#!/usr/bin/env python3
"""
Script to initialize the database with default data.

This script will:
1. Create default agents
2. Create a demo user
3. Create sample conversations and messages

Usage:
    python init_db.py --postgres-uri postgresql://postgres:postgres@localhost:5432/neuronest
"""

import argparse
import logging
import sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path so we can import the models
sys.path.append("..")
from database.models import User, Device, Conversation, Message, Agent, Log
from core.security import get_password_hash


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def connect_postgres(postgres_uri: str):
    """Connect to PostgreSQL."""
    try:
        engine = create_engine(postgres_uri)
        Session = sessionmaker(bind=engine)
        session = Session()
        # Test the connection
        session.execute("SELECT 1")
        logger.info("Connected to PostgreSQL")
        return session
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise


def create_default_agents(session):
    """Create default agents."""
    agents = [
        {
            "name": "Thinker",
            "description": "Analytical thinking and problem-solving agent",
            "model": "gpt-4",
        },
        {
            "name": "Developer",
            "description": "Code and technical problem-solving agent",
            "model": "gpt-4",
        },
        {
            "name": "Writer",
            "description": "Content creation and writing agent",
            "model": "gpt-4",
        },
        {
            "name": "Researcher",
            "description": "Information gathering and research agent",
            "model": "gpt-4",
        },
        {
            "name": "AutoGen",
            "description": "Multi-agent system using AutoGen framework",
            "model": "gpt-4",
        },
        {
            "name": "CrewAI",
            "description": "Multi-agent system using CrewAI framework",
            "model": "gpt-4",
        },
    ]
    
    for agent_data in agents:
        # Check if agent already exists
        existing_agent = session.query(Agent).filter_by(name=agent_data["name"]).first()
        if existing_agent:
            logger.info(f"Agent {agent_data['name']} already exists")
            continue
        
        # Create new agent
        new_agent = Agent(
            name=agent_data["name"],
            description=agent_data["description"],
            model=agent_data["model"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(new_agent)
        logger.info(f"Created agent {agent_data['name']}")
    
    session.commit()
    logger.info("Default agents created successfully")


def create_demo_user(session):
    """Create a demo user."""
    # Check if demo user already exists
    existing_user = session.query(User).filter_by(email="demo@example.com").first()
    if existing_user:
        logger.info("Demo user already exists")
        return existing_user
    
    # Create demo user
    demo_user = User(
        email="demo@example.com",
        username="demo",
        hashed_password=get_password_hash("password123"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(demo_user)
    session.flush()
    
    # Create a default device for the demo user
    demo_device = Device(
        user_id=demo_user.id,
        device_id="demo_device",
        device_name="Demo Device",
        device_type="web",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(demo_device)
    
    session.commit()
    logger.info("Demo user created successfully")
    return demo_user


def create_sample_conversations(session, user):
    """Create sample conversations and messages."""
    # Get agent IDs
    thinker_agent = session.query(Agent).filter_by(name="Thinker").first()
    developer_agent = session.query(Agent).filter_by(name="Developer").first()
    
    # Create sample conversations
    conversations = [
        {
            "title": "Getting Started with NeuroNest-AI",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello! I'm new to NeuroNest-AI. Can you tell me what you can do?",
                },
                {
                    "role": "assistant",
                    "content": "Welcome to NeuroNest-AI! I'm the Thinker agent, and I'm here to help you with analytical thinking and problem-solving.\n\nNeuroNest-AI is an advanced AI agent orchestration platform that enables seamless interaction with multiple specialized AI agents. Here are some things I can help you with:\n\n1. Answer questions and provide information on a wide range of topics\n2. Help you think through complex problems\n3. Analyze situations and provide insights\n4. Connect you with other specialized agents for specific tasks\n\nWhat would you like to know more about?",
                    "agent_id": thinker_agent.id if thinker_agent else None,
                },
                {
                    "role": "user",
                    "content": "Can you help me with programming?",
                },
                {
                    "role": "assistant",
                    "content": "While I can provide general guidance on programming concepts, for specific programming help, I'd recommend connecting you with our Developer agent who specializes in coding and technical problem-solving.\n\nThe Developer agent can help you with:\n\n1. Writing and debugging code in various programming languages\n2. Explaining technical concepts and algorithms\n3. Providing guidance on software architecture and design patterns\n4. Troubleshooting technical issues\n\nWould you like me to connect you with the Developer agent for your programming questions?",
                    "agent_id": thinker_agent.id if thinker_agent else None,
                },
            ],
        },
        {
            "title": "Python Programming Help",
            "messages": [
                {
                    "role": "user",
                    "content": "I need help with a Python function to calculate Fibonacci numbers.",
                },
                {
                    "role": "assistant",
                    "content": "I'd be happy to help you with a Python function to calculate Fibonacci numbers. Here's a simple recursive implementation:\n\n```python\ndef fibonacci_recursive(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:\n        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)\n```\n\nHowever, this recursive approach can be inefficient for large values of n due to repeated calculations. Here's a more efficient iterative approach:\n\n```python\ndef fibonacci_iterative(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    \n    a, b = 0, 1\n    for _ in range(2, n+1):\n        a, b = b, a + b\n    return b\n```\n\nAnd if you want even better performance for very large values, you can use memoization to cache results:\n\n```python\ndef fibonacci_memoization(n, memo={}):\n    if n in memo:\n        return memo[n]\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    \n    memo[n] = fibonacci_memoization(n-1, memo) + fibonacci_memoization(n-2, memo)\n    return memo[n]\n```\n\nWhich approach would work best for your specific use case?",
                    "agent_id": developer_agent.id if developer_agent else None,
                },
                {
                    "role": "user",
                    "content": "The iterative approach looks good. Can you explain how it works?",
                },
                {
                    "role": "assistant",
                    "content": "I'd be happy to explain how the iterative Fibonacci function works!\n\n```python\ndef fibonacci_iterative(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    \n    a, b = 0, 1\n    for _ in range(2, n+1):\n        a, b = b, a + b\n    return b\n```\n\nHere's a step-by-step explanation:\n\n1. First, we handle the base cases:\n   - If n is 0 or negative, we return 0\n   - If n is 1, we return 1\n\n2. For n ≥ 2, we use an iterative approach:\n   - We initialize two variables: `a = 0` (representing F(0)) and `b = 1` (representing F(1))\n   - We then iterate from 2 to n (inclusive)\n   - In each iteration, we update our variables:\n     - `a` becomes the previous value of `b` (the previous Fibonacci number)\n     - `b` becomes the sum of the previous values of `a` and `b` (the new Fibonacci number)\n   - After n-1 iterations, `b` will contain the nth Fibonacci number\n\n3. Finally, we return `b`, which is F(n)\n\nThe key advantage of this approach is that we only need to keep track of the two most recent Fibonacci numbers at any point, making it much more memory-efficient than storing the entire sequence.\n\nThe time complexity is O(n) since we perform a constant amount of work for each number from 2 to n. The space complexity is O(1) since we only use two variables regardless of the input size.\n\nWould you like me to walk through an example calculation to see how the values change during each iteration?",
                    "agent_id": developer_agent.id if developer_agent else None,
                },
            ],
        },
    ]
    
    for conv_data in conversations:
        # Create conversation
        new_conv = Conversation(
            user_id=user.id,
            title=conv_data["title"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(new_conv)
        session.flush()
        
        # Create messages
        for i, msg_data in enumerate(conv_data["messages"]):
            new_msg = Message(
                conversation_id=new_conv.id,
                content=msg_data["content"],
                role=msg_data["role"],
                agent_id=msg_data.get("agent_id"),
                created_at=datetime.utcnow() - (len(conv_data["messages"]) - i) * 60,  # Stagger timestamps
                updated_at=datetime.utcnow() - (len(conv_data["messages"]) - i) * 60,
            )
            session.add(new_msg)
        
        logger.info(f"Created conversation: {conv_data['title']}")
    
    session.commit()
    logger.info("Sample conversations created successfully")


def main():
    parser = argparse.ArgumentParser(description="Initialize database with default data")
    parser.add_argument("--postgres-uri", required=True, help="PostgreSQL connection URI")
    args = parser.parse_args()
    
    try:
        # Connect to PostgreSQL
        session = connect_postgres(args.postgres_uri)
        
        # Create default data
        create_default_agents(session)
        demo_user = create_demo_user(session)
        create_sample_conversations(session, demo_user)
        
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()