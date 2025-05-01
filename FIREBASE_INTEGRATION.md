# Firebase Integration

This document describes the integration of Firebase services into the NeuroNest-AI project.

## Overview

NeuroNest-AI now uses Firebase as the primary backend service for data storage and retrieval. This integration provides a modern, scalable, and real-time database solution with comprehensive features for the application.

The integration includes:

1. **Firebase Admin SDK**: For secure server-side operations and authentication
2. **Firestore**: NoSQL document database for structured data storage with real-time capabilities
3. **Firebase Storage**: For file storage, including documents, images, and other binary data
4. **Firebase Authentication**: For user management and security (optional)

The integration is designed with a hybrid approach that works alongside the existing Supabase implementation, providing a fallback mechanism for backward compatibility and ensuring a smooth transition. This approach allows for gradual migration without disrupting existing functionality.

## Setup

### Prerequisites

- Firebase project (ManusAI-Next)
- Service account credentials file
- Enabled Firebase services:
  - **Firestore Database**: Must be enabled in the Google Cloud Console
  - **Firebase Storage**: Must be created and configured in the Firebase Console

### Required Firebase Services

Before using the Firebase integration, you must enable the following services:

1. **Enable Firestore API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/library/firestore.googleapis.com)
   - Select your project (ManusAI-Next)
   - Click "Enable" to activate the Firestore API

2. **Create Firebase Storage Bucket**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your project (ManusAI-Next)
   - Navigate to "Storage" in the left sidebar
   - Click "Get Started" and follow the setup wizard

### Installation

1. Install the Firebase Admin SDK:

```bash
pip install firebase-admin
```

2. Place the service account key file in the `firebase/` directory:

```
firebase/serviceAccountKey.json
```

3. Make sure the service account key file is added to `.gitignore` to prevent accidental exposure.

## Implementation Details

### Firebase Core Module

The `app/core/firebase.py` module initializes the Firebase Admin SDK and provides low-level access to Firebase services:

- Initializes Firebase with the service account key
- Provides access to Firestore and Storage
- Includes basic CRUD operations for Firestore documents
- Includes file operations for Firebase Storage

### Firebase Service Class

A `FirebaseService` class has been implemented in the `app/core/firebase.py` module to provide a unified interface for interacting with Firebase services. This class includes:

- High-level methods for working with specific collections
- Document CRUD operations (create, read, update, delete)
- Query capabilities for filtering documents
- File storage operations (upload, download, delete)
- Error handling and logging

The class is instantiated as a singleton `firebase_service` that can be imported and used throughout the application.

### Integration with Existing Services

The following services have been updated to use Firebase:

1. **Memory Service**: Agent memories are now stored in Firestore with fallback to Supabase.
2. **Conversation Service**: Conversations and messages are stored in Firestore with fallback to Supabase.
3. **Settings Service**: User settings are stored in Firestore with fallback to in-memory storage.
4. **File Service**: File metadata and content are stored in Firestore and Firebase Storage.
5. **Project Service**: Project data is stored in Firestore.

### Data Structure

The Firebase integration uses the following Firestore collections:

- `memories`: Stores agent memory entries
- `sessions`: Stores session data
- `conversations`: Stores conversation metadata and messages
- `user_settings`: Stores user settings
- `files`: Stores file metadata and content
- `projects`: Stores project data

## Usage

### Accessing Firebase Services

To use Firebase services in your code, import the `firebase_service` singleton:

```python
from app.core.firebase import firebase_service

# Check if Firebase is initialized
if firebase_service.is_initialized():
    # Use Firebase services
    firebase_service.create_document("collection_name", data, document_id)
    
    # Get a document
    document = firebase_service.get_document("collection_name", document_id)
    
    # Update a document
    firebase_service.update_document("collection_name", document_id, {"updated": True})
    
    # Delete a document
    firebase_service.delete_document("collection_name", document_id)
    
    # Query documents
    documents = firebase_service.query_documents("collection_name", 
                                               field="user_id", 
                                               operator="==", 
                                               value="user123")
```

### Working with Collections

The Firebase integration uses specific collections for different types of data:

#### Sessions

```python
# Save a session
firebase_service.create_document("sessions", session_data, session_id)

# Get a session
session_data = firebase_service.get_document("sessions", session_id)

# Update a session
firebase_service.update_document("sessions", session_id, {"last_active": "2023-01-01T00:00:00Z"})
```

#### Memories

```python
# Save a memory
firebase_service.create_document("memories", memory_data, memory_id)

# Get memories for a specific agent
memories = firebase_service.query_documents("memories", 
                                          field="agent_id", 
                                          operator="==", 
                                          value="agent123")
```

#### Files

```python
# Upload a file
url = firebase_service.upload_file("/path/to/local/file.txt", "remote/path/file.txt")

# Download a file
firebase_service.download_file("remote/path/file.txt", "/path/to/local/file.txt")
```

## Configuration

Firebase configuration is managed through environment variables and the default service account key file:

1. `FIREBASE_CREDENTIALS`: Path to the service account key file or JSON string of credentials
2. `FIREBASE_WEB_API_KEY`: Firebase Web API key for client-side operations

If `FIREBASE_CREDENTIALS` is not provided, the system will look for the service account key file at `firebase/serviceAccountKey.json`.

## Security Rules

For development purposes, the following Firestore security rules can be used:

```
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**Note**: These rules allow unrestricted access and should be replaced with proper security rules in production.

## Fallback Mechanism

The Firebase integration includes a fallback mechanism to ensure backward compatibility:

1. If Firebase is not initialized or an operation fails, the system will fall back to the existing implementation (Supabase or in-memory storage).
2. For critical operations, data is stored in both Firebase and Supabase to ensure consistency during the transition period.

## Future Improvements

1. **Security Enhancements**:
   - Implement more sophisticated security rules for Firestore
   - Add role-based access control
   - Implement data encryption for sensitive information

2. **Authentication Integration**:
   - Enhance Firebase Authentication integration
   - Implement OAuth providers (Google, GitHub, etc.)
   - Add multi-factor authentication

3. **Real-time Features**:
   - Implement real-time updates using Firestore listeners
   - Add WebSocket support for live notifications
   - Create collaborative features using real-time database

4. **Performance Optimization**:
   - Optimize query performance for large datasets
   - Implement caching for frequently accessed data
   - Add pagination for large result sets
   - Optimize indexing for common queries

5. **Development Improvements**:
   - Add comprehensive unit tests for Firebase integration
   - Set up CI/CD for Firebase deployment
   - Implement automated testing for Firebase functions
   - Create development, staging, and production environments

6. **Advanced Features**:
   - Add Firebase Functions for serverless operations
   - Implement Firebase Cloud Messaging for notifications
   - Add Firebase Analytics for usage tracking
   - Implement Firebase Remote Config for feature flags

7. **Resilience and Reliability**:
   - Add more comprehensive error handling and retry mechanisms
   - Implement circuit breakers for external service calls
   - Add monitoring and alerting for Firebase services
   - Create disaster recovery procedures