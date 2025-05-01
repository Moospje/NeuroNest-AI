"""
Conversation Service
Handles conversation storage and retrieval
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid
import logging

from app.database.supabase_client import get_supabase_client
from app.services.firebase_service import firebase_service

logger = logging.getLogger(__name__)


async def create_conversation(
    user_id: str,
    title: Optional[str] = None,
    context: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a new conversation
    
    Args:
        user_id: User ID
        title: Optional conversation title
        context: Optional conversation context
        metadata: Optional metadata
        
    Returns:
        Created conversation
    """
    conversation_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    # Generate title if not provided
    if not title:
        title = f"Conversation {now}"
    
    conversation_data = {
        "id": conversation_id,
        "user_id": user_id,
        "title": title,
        "context": context or "",
        "metadata": json.dumps(metadata) if metadata else "{}",
        "created_at": now,
        "updated_at": now
    }
    
    # Try to store in Firebase first
    if firebase_service.is_initialized():
        doc_id = firebase_service.save_document("conversations", conversation_data, conversation_id)
        if doc_id:
            conversation = conversation_data
            logger.info(f"Conversation stored in Firebase with ID: {doc_id}")
            
            # Parse metadata JSON
            if conversation.get("metadata") and isinstance(conversation["metadata"], str):
                try:
                    conversation["metadata"] = json.loads(conversation["metadata"])
                except json.JSONDecodeError:
                    conversation["metadata"] = {}
            
            return conversation
        else:
            logger.warning("Failed to store conversation in Firebase, falling back to Supabase")
    
    # Fall back to Supabase
    supabase = get_supabase_client()
    response = supabase.table("conversations").insert(conversation_data).execute()
    
    if not response.data or len(response.data) == 0:
        raise Exception("Failed to create conversation")
    
    conversation = response.data[0]
    
    # Parse metadata JSON
    if conversation.get("metadata") and isinstance(conversation["metadata"], str):
        try:
            conversation["metadata"] = json.loads(conversation["metadata"])
        except json.JSONDecodeError:
            conversation["metadata"] = {}
    
    return conversation


async def get_conversations(
    user_id: str,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get conversations for a user
    
    Args:
        user_id: User ID
        limit: Maximum number of conversations to return
        offset: Offset for pagination
        
    Returns:
        List of conversations
    """
    # Try to get conversations from Firebase first
    if firebase_service.is_initialized():
        # Build filters
        filters = [("user_id", "==", user_id)]
        
        # Query Firebase
        conversations = firebase_service.query_documents(
            collection="conversations",
            filters=filters,
            order_by=("updated_at", "DESCENDING"),
            limit=limit,
            offset=offset
        )
        
        if conversations:
            # Parse metadata JSON if needed
            for conversation in conversations:
                if conversation.get("metadata") and isinstance(conversation["metadata"], str):
                    try:
                        conversation["metadata"] = json.loads(conversation["metadata"])
                    except json.JSONDecodeError:
                        conversation["metadata"] = {}
            
            return conversations
        else:
            logger.warning("No conversations found in Firebase or query failed, falling back to Supabase")
    
    # Fall back to Supabase
    supabase = get_supabase_client()
    
    response = supabase.table("conversations").select("*").eq("user_id", user_id).order("updated_at", desc=True).limit(limit).offset(offset).execute()
    
    if not response.data:
        return []
    
    # Parse metadata JSON
    for conversation in response.data:
        if conversation.get("metadata") and isinstance(conversation["metadata"], str):
            try:
                conversation["metadata"] = json.loads(conversation["metadata"])
            except json.JSONDecodeError:
                conversation["metadata"] = {}
    
    return response.data


async def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a conversation by ID
    
    Args:
        conversation_id: Conversation ID
        
    Returns:
        Conversation or None if not found
    """
    # Try to get conversation from Firebase first
    if firebase_service.is_initialized():
        conversation = firebase_service.get_document("conversations", conversation_id)
        if conversation:
            # Parse metadata JSON if needed
            if conversation.get("metadata") and isinstance(conversation["metadata"], str):
                try:
                    conversation["metadata"] = json.loads(conversation["metadata"])
                except json.JSONDecodeError:
                    conversation["metadata"] = {}
            
            return conversation
        else:
            logger.warning(f"Conversation {conversation_id} not found in Firebase, falling back to Supabase")
    
    # Fall back to Supabase
    supabase = get_supabase_client()
    
    response = supabase.table("conversations").select("*").eq("id", conversation_id).execute()
    
    if not response.data or len(response.data) == 0:
        return None
    
    conversation = response.data[0]
    
    # Parse metadata JSON
    if conversation.get("metadata") and isinstance(conversation["metadata"], str):
        try:
            conversation["metadata"] = json.loads(conversation["metadata"])
        except json.JSONDecodeError:
            conversation["metadata"] = {}
    
    return conversation


async def update_conversation(
    conversation_id: str,
    title: Optional[str] = None,
    context: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Update a conversation
    
    Args:
        conversation_id: Conversation ID
        title: Optional new title
        context: Optional new context
        metadata: Optional new metadata
        
    Returns:
        Updated conversation or None if not found
    """
    # Get current conversation to merge metadata
    current_conversation = await get_conversation(conversation_id)
    
    if not current_conversation:
        return None
    
    update_data = {
        "updated_at": datetime.utcnow().isoformat()
    }
    
    if title is not None:
        update_data["title"] = title
    
    if context is not None:
        update_data["context"] = context
    
    if metadata is not None:
        # Merge with existing metadata
        current_metadata = current_conversation.get("metadata", {})
        merged_metadata = {**current_metadata, **metadata}
        update_data["metadata"] = json.dumps(merged_metadata)
    
    # Try to update in Firebase first
    conversation = None
    if firebase_service.is_initialized():
        success = firebase_service.update_document("conversations", conversation_id, update_data)
        if success:
            # Get the updated conversation
            conversation = firebase_service.get_document("conversations", conversation_id)
            logger.info(f"Conversation updated in Firebase with ID: {conversation_id}")
            
            # Parse metadata JSON if needed
            if conversation and conversation.get("metadata") and isinstance(conversation["metadata"], str):
                try:
                    conversation["metadata"] = json.loads(conversation["metadata"])
                except json.JSONDecodeError:
                    conversation["metadata"] = {}
        else:
            logger.warning(f"Failed to update conversation {conversation_id} in Firebase, falling back to Supabase")
    
    # Fall back to Supabase if Firebase update failed or not initialized
    if not conversation:
        supabase = get_supabase_client()
        response = supabase.table("conversations").update(update_data).eq("id", conversation_id).execute()
        
        if not response.data or len(response.data) == 0:
            return None
        
        conversation = response.data[0]
        
        # Parse metadata JSON
        if conversation.get("metadata") and isinstance(conversation["metadata"], str):
            try:
                conversation["metadata"] = json.loads(conversation["metadata"])
            except json.JSONDecodeError:
                conversation["metadata"] = {}
    
    return conversation


async def delete_conversation(conversation_id: str) -> bool:
    """
    Delete a conversation
    
    Args:
        conversation_id: Conversation ID
        
    Returns:
        True if deleted, False otherwise
    """
    # First, delete all messages in the conversation
    await delete_conversation_messages(conversation_id)
    
    success = False
    
    # Try to delete from Firebase first
    if firebase_service.is_initialized():
        firebase_success = firebase_service.delete_document("conversations", conversation_id)
        if firebase_success:
            success = True
            logger.info(f"Conversation deleted from Firebase with ID: {conversation_id}")
        else:
            logger.warning(f"Failed to delete conversation {conversation_id} from Firebase, falling back to Supabase")
    
    # Also try to delete from Supabase (to ensure data consistency)
    supabase = get_supabase_client()
    response = supabase.table("conversations").delete().eq("id", conversation_id).execute()
    if response.data is not None and len(response.data) > 0:
        success = True
    
    return success


async def add_message_to_conversation(
    conversation_id: str,
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Add a message to a conversation
    
    Args:
        conversation_id: Conversation ID
        role: Message role (e.g., "user", "assistant", "system")
        content: Message content
        metadata: Optional message metadata
        
    Returns:
        Created message
    """
    # Check if conversation exists
    conversation = await get_conversation(conversation_id)
    
    if not conversation:
        raise Exception("Conversation not found")
    
    message_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    message_data = {
        "id": message_id,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "metadata": json.dumps(metadata) if metadata else "{}",
        "created_at": now
    }
    
    # Try to store in Firebase first
    if firebase_service.is_initialized():
        doc_id = firebase_service.save_document("conversation_messages", message_data, message_id)
        if doc_id:
            message = message_data
            logger.info(f"Message stored in Firebase with ID: {doc_id}")
            
            # Parse metadata JSON
            if message.get("metadata") and isinstance(message["metadata"], str):
                try:
                    message["metadata"] = json.loads(message["metadata"])
                except json.JSONDecodeError:
                    message["metadata"] = {}
            
            # Update conversation updated_at
            await update_conversation(conversation_id)
            
            return message
        else:
            logger.warning("Failed to store message in Firebase, falling back to Supabase")
    
    # Fall back to Supabase
    supabase = get_supabase_client()
    response = supabase.table("conversation_messages").insert(message_data).execute()
    
    if not response.data or len(response.data) == 0:
        raise Exception("Failed to add message to conversation")
    
    message = response.data[0]
    
    # Parse metadata JSON
    if message.get("metadata") and isinstance(message["metadata"], str):
        try:
            message["metadata"] = json.loads(message["metadata"])
        except json.JSONDecodeError:
            message["metadata"] = {}
    
    # Update conversation updated_at
    await update_conversation(conversation_id)
    
    return message


async def get_conversation_messages(
    conversation_id: str,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get messages for a conversation
    
    Args:
        conversation_id: Conversation ID
        limit: Maximum number of messages to return
        offset: Offset for pagination
        
    Returns:
        List of messages
    """
    # Try to get messages from Firebase first
    if firebase_service.is_initialized():
        # Build filters
        filters = [("conversation_id", "==", conversation_id)]
        
        # Query Firebase
        messages = firebase_service.query_documents(
            collection="conversation_messages",
            filters=filters,
            order_by=("created_at", "ASCENDING"),
            limit=limit,
            offset=offset
        )
        
        if messages:
            # Parse metadata JSON if needed
            for message in messages:
                if message.get("metadata") and isinstance(message["metadata"], str):
                    try:
                        message["metadata"] = json.loads(message["metadata"])
                    except json.JSONDecodeError:
                        message["metadata"] = {}
            
            return messages
        else:
            logger.warning(f"No messages found in Firebase for conversation {conversation_id}, falling back to Supabase")
    
    # Fall back to Supabase
    supabase = get_supabase_client()
    
    response = supabase.table("conversation_messages").select("*").eq("conversation_id", conversation_id).order("created_at", desc=False).limit(limit).offset(offset).execute()
    
    if not response.data:
        return []
    
    # Parse metadata JSON
    for message in response.data:
        if message.get("metadata") and isinstance(message["metadata"], str):
            try:
                message["metadata"] = json.loads(message["metadata"])
            except json.JSONDecodeError:
                message["metadata"] = {}
    
    return response.data


async def delete_conversation_messages(conversation_id: str) -> bool:
    """
    Delete all messages in a conversation
    
    Args:
        conversation_id: Conversation ID
        
    Returns:
        True if deleted, False otherwise
    """
    success = False
    
    # Try to delete from Firebase first
    if firebase_service.is_initialized():
        # Get all messages for this conversation
        messages = await get_conversation_messages(conversation_id)
        message_ids = [message["id"] for message in messages]
        
        # Delete each message individually from Firebase
        if message_ids:
            firebase_success = True
            for message_id in message_ids:
                if not firebase_service.delete_document("conversation_messages", message_id):
                    firebase_success = False
            
            if firebase_success:
                success = True
                logger.info(f"Deleted {len(message_ids)} messages from Firebase for conversation {conversation_id}")
            else:
                logger.warning(f"Failed to delete all messages from Firebase for conversation {conversation_id}, falling back to Supabase")
    
    # Also delete from Supabase (to ensure data consistency)
    supabase = get_supabase_client()
    response = supabase.table("conversation_messages").delete().eq("conversation_id", conversation_id).execute()
    if response.data is not None:
        success = True
    
    return success