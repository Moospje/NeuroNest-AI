#!/usr/bin/env python3
"""
Script to migrate data from the old NeuroNest-AI structure to the new one.

This script will:
1. Connect to the old MongoDB database
2. Extract users, conversations, and messages
3. Convert them to the new PostgreSQL schema
4. Insert them into the new PostgreSQL database

Usage:
    python migrate_data.py --mongo-uri mongodb://localhost:27017 --postgres-uri postgresql://postgres:postgres@localhost:5432/neuronest
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

import pymongo
from pymongo import MongoClient
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


def connect_mongo(mongo_uri: str) -> MongoClient:
    """Connect to MongoDB."""
    try:
        client = MongoClient(mongo_uri)
        # Test the connection
        client.admin.command("ping")
        logger.info("Connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


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


def get_mongo_users(mongo_client: MongoClient) -> List[Dict[str, Any]]:
    """Get users from MongoDB."""
    db = mongo_client.neuronest
    users = list(db.users.find())
    logger.info(f"Found {len(users)} users in MongoDB")
    return users


def get_mongo_conversations(mongo_client: MongoClient) -> List[Dict[str, Any]]:
    """Get conversations from MongoDB."""
    db = mongo_client.neuronest
    conversations = list(db.conversations.find())
    logger.info(f"Found {len(conversations)} conversations in MongoDB")
    return conversations


def get_mongo_messages(mongo_client: MongoClient) -> List[Dict[str, Any]]:
    """Get messages from MongoDB."""
    db = mongo_client.neuronest
    messages = list(db.messages.find())
    logger.info(f"Found {len(messages)} messages in MongoDB")
    return messages


def migrate_users(mongo_users: List[Dict[str, Any]], postgres_session) -> Dict[str, int]:
    """Migrate users from MongoDB to PostgreSQL."""
    user_id_map = {}  # Map MongoDB user IDs to PostgreSQL user IDs
    
    for mongo_user in mongo_users:
        # Check if user already exists in PostgreSQL
        existing_user = postgres_session.query(User).filter_by(email=mongo_user.get("email")).first()
        if existing_user:
            user_id_map[str(mongo_user["_id"])] = existing_user.id
            logger.info(f"User {mongo_user.get('email')} already exists in PostgreSQL")
            continue
        
        # Create new user
        new_user = User(
            email=mongo_user.get("email"),
            username=mongo_user.get("username"),
            hashed_password=get_password_hash(mongo_user.get("password", "password123")),
            created_at=mongo_user.get("created_at", datetime.utcnow()),
            updated_at=mongo_user.get("updated_at", datetime.utcnow()),
        )
        postgres_session.add(new_user)
        postgres_session.flush()  # Get the ID without committing
        
        # Create a default device for the user
        new_device = Device(
            user_id=new_user.id,
            device_id=mongo_user.get("device_id", "default_device"),
            device_name=mongo_user.get("device_name", "Default Device"),
            device_type=mongo_user.get("device_type", "unknown"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        postgres_session.add(new_device)
        
        user_id_map[str(mongo_user["_id"])] = new_user.id
        logger.info(f"Migrated user {mongo_user.get('email')}")
    
    postgres_session.commit()
    logger.info(f"Migrated {len(user_id_map)} users to PostgreSQL")
    return user_id_map


def migrate_conversations(
    mongo_conversations: List[Dict[str, Any]], 
    user_id_map: Dict[str, int], 
    postgres_session
) -> Dict[str, int]:
    """Migrate conversations from MongoDB to PostgreSQL."""
    conversation_id_map = {}  # Map MongoDB conversation IDs to PostgreSQL conversation IDs
    
    for mongo_conv in mongo_conversations:
        mongo_user_id = mongo_conv.get("user_id")
        if not mongo_user_id or str(mongo_user_id) not in user_id_map:
            logger.warning(f"Skipping conversation {mongo_conv.get('_id')}: User not found")
            continue
        
        user_id = user_id_map[str(mongo_user_id)]
        
        # Create new conversation
        new_conv = Conversation(
            user_id=user_id,
            title=mongo_conv.get("title", "Untitled Conversation"),
            created_at=mongo_conv.get("created_at", datetime.utcnow()),
            updated_at=mongo_conv.get("updated_at", datetime.utcnow()),
        )
        postgres_session.add(new_conv)
        postgres_session.flush()  # Get the ID without committing
        
        conversation_id_map[str(mongo_conv["_id"])] = new_conv.id
        logger.info(f"Migrated conversation {mongo_conv.get('title')}")
    
    postgres_session.commit()
    logger.info(f"Migrated {len(conversation_id_map)} conversations to PostgreSQL")
    return conversation_id_map


def migrate_messages(
    mongo_messages: List[Dict[str, Any]], 
    conversation_id_map: Dict[str, int], 
    postgres_session
) -> None:
    """Migrate messages from MongoDB to PostgreSQL."""
    message_count = 0
    
    # Get or create default agents
    thinker_agent = postgres_session.query(Agent).filter_by(name="Thinker").first()
    if not thinker_agent:
        thinker_agent = Agent(
            name="Thinker",
            description="Analytical thinking and problem-solving agent",
            model="gpt-4",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        postgres_session.add(thinker_agent)
        postgres_session.flush()
    
    developer_agent = postgres_session.query(Agent).filter_by(name="Developer").first()
    if not developer_agent:
        developer_agent = Agent(
            name="Developer",
            description="Code and technical problem-solving agent",
            model="gpt-4",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        postgres_session.add(developer_agent)
        postgres_session.flush()
    
    # Map agent names to IDs
    agent_map = {
        "thinker": thinker_agent.id,
        "developer": developer_agent.id,
    }
    
    for mongo_msg in mongo_messages:
        mongo_conv_id = mongo_msg.get("conversation_id")
        if not mongo_conv_id or str(mongo_conv_id) not in conversation_id_map:
            logger.warning(f"Skipping message {mongo_msg.get('_id')}: Conversation not found")
            continue
        
        conversation_id = conversation_id_map[str(mongo_conv_id)]
        
        # Get agent ID if applicable
        agent_id = None
        if mongo_msg.get("role") == "assistant" and mongo_msg.get("agent"):
            agent_id = agent_map.get(mongo_msg.get("agent"))
        
        # Create new message
        new_msg = Message(
            conversation_id=conversation_id,
            content=mongo_msg.get("content", ""),
            role=mongo_msg.get("role", "user"),
            agent_id=agent_id,
            created_at=mongo_msg.get("created_at", datetime.utcnow()),
            updated_at=mongo_msg.get("updated_at", datetime.utcnow()),
        )
        postgres_session.add(new_msg)
        message_count += 1
        
        # Commit in batches to avoid memory issues
        if message_count % 100 == 0:
            postgres_session.commit()
            logger.info(f"Migrated {message_count} messages so far")
    
    postgres_session.commit()
    logger.info(f"Migrated {message_count} messages to PostgreSQL")


def main():
    parser = argparse.ArgumentParser(description="Migrate data from MongoDB to PostgreSQL")
    parser.add_argument("--mongo-uri", required=True, help="MongoDB connection URI")
    parser.add_argument("--postgres-uri", required=True, help="PostgreSQL connection URI")
    args = parser.parse_args()
    
    try:
        # Connect to databases
        mongo_client = connect_mongo(args.mongo_uri)
        postgres_session = connect_postgres(args.postgres_uri)
        
        # Get data from MongoDB
        mongo_users = get_mongo_users(mongo_client)
        mongo_conversations = get_mongo_conversations(mongo_client)
        mongo_messages = get_mongo_messages(mongo_client)
        
        # Migrate data to PostgreSQL
        user_id_map = migrate_users(mongo_users, postgres_session)
        conversation_id_map = migrate_conversations(mongo_conversations, user_id_map, postgres_session)
        migrate_messages(mongo_messages, conversation_id_map, postgres_session)
        
        logger.info("Migration completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    main()