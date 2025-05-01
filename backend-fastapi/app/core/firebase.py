import json
import os
import logging
from typing import Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
from app.config import settings

logger = logging.getLogger(__name__)

# Create a class for Firebase service
class FirebaseService:
    """
    Firebase Service for interacting with Firestore and Storage
    """
    
    def __init__(self):
        """Initialize Firebase Service"""
        self.initialized = False
        self.db = None
        self.bucket = None
        
        # Initialize Firebase if not already initialized
        if not firebase_app:
            initialize_firebase()
            
        # Set instance variables
        self.initialized = firebase_app is not None
        self.db = db
        self.bucket = bucket
    
    def is_initialized(self) -> bool:
        """Check if Firebase is initialized"""
        return self.initialized and self.db is not None
    
    def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document from Firestore"""
        return get_document(collection, doc_id)
    
    def create_document(self, collection: str, data: Dict[str, Any]) -> Optional[str]:
        """Create a document in Firestore"""
        return add_document(collection, data)
    
    def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update a document in Firestore"""
        return update_document(collection, doc_id, data)
    
    def delete_document(self, collection: str, doc_id: str) -> bool:
        """Delete a document from Firestore"""
        return delete_document(collection, doc_id)
    
    def query_documents(self, collection: str, field: str, operator: str, value: Any) -> Optional[list]:
        """Query documents from Firestore"""
        return query_documents(collection, field, operator, value)
    
    def upload_file(self, file_path: str, destination_path: str) -> Optional[str]:
        """Upload a file to Firebase Storage"""
        return upload_file(file_path, destination_path)
    
    def download_file(self, source_path: str, destination_path: str) -> bool:
        """Download a file from Firebase Storage"""
        return download_file(source_path, destination_path)
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from Firebase Storage"""
        return delete_file(file_path)

# Initialize Firebase Admin SDK
firebase_app = None
db = None
bucket = None

def initialize_firebase():
    """
    Initialize Firebase Admin SDK
    """
    global firebase_app, db, bucket
    
    try:
        # Default path to the service account key
        default_credentials_path = "/workspace/NeuroNest-AI/firebase/serviceAccountKey.json"
        
        # Check if Firebase credentials are provided
        if hasattr(settings, 'firebase_credentials') and settings.firebase_credentials:
            # If credentials are provided as a JSON string
            if settings.firebase_credentials.startswith('{'):
                cred_dict = json.loads(settings.firebase_credentials)
                cred = credentials.Certificate(cred_dict)
            # If credentials are provided as a path to a JSON file
            else:
                cred = credentials.Certificate(settings.firebase_credentials)
        elif os.path.exists(default_credentials_path):
            # Use the default credentials file if it exists
            cred = credentials.Certificate(default_credentials_path)
            logger.info(f"Using default Firebase credentials from {default_credentials_path}")
        else:
            logger.warning("Firebase credentials not provided. Firebase functionality will be limited.")
            return
                
        # Initialize Firebase Admin SDK with storage bucket
        try:
            firebase_app = firebase_admin.initialize_app(cred, {
                'storageBucket': 'manusai-next.appspot.com'
            })
        except ValueError as e:
            logger.warning(f"Firebase Storage initialization failed: {e}")
            firebase_app = firebase_admin.initialize_app(cred)
            
        db = firestore.client()
        
        # Initialize Storage bucket if available
        try:
            bucket = storage.bucket()
        except Exception as e:
            logger.warning(f"Firebase Storage initialization failed: {e}")
            
        logger.info("Firebase Admin SDK initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Firebase Admin SDK: {e}")
        
# Initialize Firebase on module import
initialize_firebase()

# Create a singleton instance of FirebaseService
firebase_service = FirebaseService()

# Firebase Authentication functions
def verify_firebase_token(id_token: str) -> Dict[str, Any]:
    """
    Verify a Firebase ID token and return the decoded token
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.error(f"Error verifying Firebase token: {e}")
        raise

def get_user_by_email(email: str) -> Dict[str, Any]:
    """
    Get a user by email
    """
    try:
        user = auth.get_user_by_email(email)
        return user.__dict__
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        raise

def get_user_by_uid(uid: str) -> Dict[str, Any]:
    """
    Get a user by UID
    """
    try:
        user = auth.get_user(uid)
        return user.__dict__
    except Exception as e:
        logger.error(f"Error getting user by UID: {e}")
        raise

def create_user(email: str, password: str, display_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new user
    """
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return user.__dict__
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise

def update_user(uid: str, **kwargs) -> Dict[str, Any]:
    """
    Update a user
    """
    try:
        user = auth.update_user(uid, **kwargs)
        return user.__dict__
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise

def delete_user(uid: str) -> None:
    """
    Delete a user
    """
    try:
        auth.delete_user(uid)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise

# Firestore functions
def get_document(collection: str, document_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a document from Firestore
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
        logger.error(f"Error getting document: {e}")
        return None

def add_document(collection: str, data: Dict[str, Any]) -> Optional[str]:
    """
    Add a document to Firestore
    """
    if not db:
        logger.warning("Firestore not initialized")
        return None
        
    try:
        doc_ref = db.collection(collection).document()
        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        return None

def update_document(collection: str, document_id: str, data: Dict[str, Any]) -> bool:
    """
    Update a document in Firestore
    """
    if not db:
        logger.warning("Firestore not initialized")
        return False
        
    try:
        doc_ref = db.collection(collection).document(document_id)
        doc_ref.update(data)
        return True
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        return False

def delete_document(collection: str, document_id: str) -> bool:
    """
    Delete a document from Firestore
    """
    if not db:
        logger.warning("Firestore not initialized")
        return False
        
    try:
        doc_ref = db.collection(collection).document(document_id)
        doc_ref.delete()
        return True
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return False

def query_documents(collection: str, field: str, operator: str, value: Any) -> Optional[list]:
    """
    Query documents from Firestore
    """
    if not db:
        logger.warning("Firestore not initialized")
        return None
        
    try:
        docs = db.collection(collection).where(field, operator, value).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        logger.error(f"Error querying documents: {e}")
        return None

# Storage functions
def upload_file(file_path: str, destination_path: str) -> Optional[str]:
    """
    Upload a file to Firebase Storage
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
        logger.error(f"Error uploading file: {e}")
        return None

def download_file(source_path: str, destination_path: str) -> bool:
    """
    Download a file from Firebase Storage
    """
    if not bucket:
        logger.warning("Firebase Storage not initialized")
        return False
        
    try:
        blob = bucket.blob(source_path)
        blob.download_to_filename(destination_path)
        return True
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return False

def delete_file(file_path: str) -> bool:
    """
    Delete a file from Firebase Storage
    """
    if not bucket:
        logger.warning("Firebase Storage not initialized")
        return False
        
    try:
        blob = bucket.blob(file_path)
        blob.delete()
        return True
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return False