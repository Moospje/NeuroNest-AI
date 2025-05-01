"""
Firebase Service
Provides a unified interface for interacting with Firebase services
"""

import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json
import uuid

from app.core.firebase import db, bucket

logger = logging.getLogger(__name__)

class FirebaseService:
    """
    Service for interacting with Firebase Firestore and Storage
    """
    
    @staticmethod
    def is_initialized() -> bool:
        """
        Check if Firebase is initialized
        
        Returns:
            bool: True if Firebase is initialized, False otherwise
        """
        return db is not None
    
    @staticmethod
    def save_document(collection: str, data: Dict[str, Any], document_id: Optional[str] = None) -> Optional[str]:
        """
        Save a document to Firestore
        
        Args:
            collection: Collection name
            data: Document data
            document_id: Optional document ID (if not provided, a new ID will be generated)
            
        Returns:
            str: Document ID or None if failed
        """
        if not db:
            logger.warning("Firestore not initialized")
            return None
            
        try:
            # Generate ID if not provided
            if not document_id:
                document_id = str(uuid.uuid4())
                
            # Add timestamps
            now = datetime.utcnow().isoformat()
            if 'created_at' not in data:
                data['created_at'] = now
            data['updated_at'] = now
            
            # Convert any JSON strings in metadata to dicts
            if 'metadata' in data and isinstance(data['metadata'], str):
                try:
                    data['metadata'] = json.loads(data['metadata'])
                except json.JSONDecodeError:
                    pass
            
            # Save document
            doc_ref = db.collection(collection).document(document_id)
            doc_ref.set(data)
            
            return document_id
        except Exception as e:
            logger.error(f"Error saving document to Firestore: {e}")
            return None
    
    @staticmethod
    def get_document(collection: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document from Firestore
        
        Args:
            collection: Collection name
            document_id: Document ID
            
        Returns:
            Dict: Document data or None if not found
        """
        if not db:
            logger.warning("Firestore not initialized")
            return None
            
        try:
            doc_ref = db.collection(collection).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting document from Firestore: {e}")
            return None
    
    @staticmethod
    def update_document(collection: str, document_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a document in Firestore
        
        Args:
            collection: Collection name
            document_id: Document ID
            data: Document data to update
            
        Returns:
            bool: True if updated, False otherwise
        """
        if not db:
            logger.warning("Firestore not initialized")
            return False
            
        try:
            # Add updated timestamp
            data['updated_at'] = datetime.utcnow().isoformat()
            
            # Convert any JSON strings in metadata to dicts
            if 'metadata' in data and isinstance(data['metadata'], str):
                try:
                    data['metadata'] = json.loads(data['metadata'])
                except json.JSONDecodeError:
                    pass
            
            # Update document
            doc_ref = db.collection(collection).document(document_id)
            doc_ref.update(data)
            
            return True
        except Exception as e:
            logger.error(f"Error updating document in Firestore: {e}")
            return False
    
    @staticmethod
    def delete_document(collection: str, document_id: str) -> bool:
        """
        Delete a document from Firestore
        
        Args:
            collection: Collection name
            document_id: Document ID
            
        Returns:
            bool: True if deleted, False otherwise
        """
        if not db:
            logger.warning("Firestore not initialized")
            return False
            
        try:
            doc_ref = db.collection(collection).document(document_id)
            doc_ref.delete()
            
            return True
        except Exception as e:
            logger.error(f"Error deleting document from Firestore: {e}")
            return False
    
    @staticmethod
    def query_documents(
        collection: str, 
        filters: Optional[List[tuple]] = None, 
        order_by: Optional[tuple] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query documents from Firestore
        
        Args:
            collection: Collection name
            filters: Optional list of filter tuples (field, operator, value)
            order_by: Optional tuple (field, direction) for ordering
            limit: Optional maximum number of documents to return
            offset: Optional offset for pagination
            
        Returns:
            List[Dict]: List of document data
        """
        if not db:
            logger.warning("Firestore not initialized")
            return []
            
        try:
            # Start query
            query = db.collection(collection)
            
            # Apply filters
            if filters:
                for field, operator, value in filters:
                    query = query.where(field, operator, value)
            
            # Apply ordering
            if order_by:
                field, direction = order_by
                query = query.order_by(field, direction=direction)
            
            # Apply limit and offset
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            # Execute query
            docs = query.stream()
            
            # Convert to list of dicts
            result = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                result.append(data)
            
            return result
        except Exception as e:
            logger.error(f"Error querying documents from Firestore: {e}")
            return []
    
    @staticmethod
    def save_session(session_id: str, data: Dict[str, Any]) -> bool:
        """
        Save a session to Firestore
        
        Args:
            session_id: Session ID
            data: Session data
            
        Returns:
            bool: True if saved, False otherwise
        """
        return FirebaseService.save_document('sessions', data, session_id) is not None
    
    @staticmethod
    def get_session(session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a session from Firestore
        
        Args:
            session_id: Session ID
            
        Returns:
            Dict: Session data or None if not found
        """
        return FirebaseService.get_document('sessions', session_id)
    
    @staticmethod
    def update_session(session_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a session in Firestore
        
        Args:
            session_id: Session ID
            data: Session data to update
            
        Returns:
            bool: True if updated, False otherwise
        """
        return FirebaseService.update_document('sessions', session_id, data)
    
    @staticmethod
    def delete_session(session_id: str) -> bool:
        """
        Delete a session from Firestore
        
        Args:
            session_id: Session ID
            
        Returns:
            bool: True if deleted, False otherwise
        """
        return FirebaseService.delete_document('sessions', session_id)
    
    @staticmethod
    def upload_file(file_path: str, destination_path: str) -> Optional[str]:
        """
        Upload a file to Firebase Storage
        
        Args:
            file_path: Local file path
            destination_path: Destination path in Firebase Storage
            
        Returns:
            str: Public URL of the uploaded file or None if failed
        """
        if not bucket:
            logger.warning("Firebase Storage not initialized")
            return None
            
        try:
            blob = bucket.blob(destination_path)
            blob.upload_from_filename(file_path)
            blob.make_public()
            
            return blob.public_url
        except Exception as e:
            logger.error(f"Error uploading file to Firebase Storage: {e}")
            return None
    
    @staticmethod
    def download_file(source_path: str, destination_path: str) -> bool:
        """
        Download a file from Firebase Storage
        
        Args:
            source_path: Source path in Firebase Storage
            destination_path: Local destination path
            
        Returns:
            bool: True if downloaded, False otherwise
        """
        if not bucket:
            logger.warning("Firebase Storage not initialized")
            return False
            
        try:
            blob = bucket.blob(source_path)
            blob.download_to_filename(destination_path)
            
            return True
        except Exception as e:
            logger.error(f"Error downloading file from Firebase Storage: {e}")
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file from Firebase Storage
        
        Args:
            file_path: Path in Firebase Storage
            
        Returns:
            bool: True if deleted, False otherwise
        """
        if not bucket:
            logger.warning("Firebase Storage not initialized")
            return False
            
        try:
            blob = bucket.blob(file_path)
            blob.delete()
            
            return True
        except Exception as e:
            logger.error(f"Error deleting file from Firebase Storage: {e}")
            return False

# Create a singleton instance
firebase_service = FirebaseService()