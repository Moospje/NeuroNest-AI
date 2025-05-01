# Firebase Integration

This document describes the integration of Firebase services into the NeuroNest-AI project.

## Overview

NeuroNest-AI now supports Firebase as a backend service for data storage and retrieval. The integration includes:

1. Firebase Admin SDK for server-side operations
2. Firestore for database operations
3. Firebase Storage for file storage (when available)

The integration is designed to work alongside the existing Supabase implementation, providing a fallback mechanism for backward compatibility.

## Setup

### Prerequisites

- Firebase project (ManusAI-Next)
- Service account credentials file

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

### Firebase Service Module

A new module `firebase_service.py` has been created to provide a unified interface for interacting with Firebase services. This module includes:

- Functions for initializing Firebase Admin SDK
- CRUD operations for Firestore documents
- File upload/download operations for Firebase Storage

### Integration with Existing Services

The following services have been updated to use Firebase:

1. **Memory Service**: Agent memories are now stored in Firestore with fallback to Supabase.
2. **Conversation Service**: Conversations and messages are stored in Firestore with fallback to Supabase.
3. **Settings Service**: User settings are stored in Firestore with fallback to in-memory storage.

### Data Structure

The Firebase integration uses the following Firestore collections:

- `agent_memories`: Stores agent memory entries
- `conversations`: Stores conversation metadata
- `conversation_messages`: Stores individual messages within conversations
- `user_settings`: Stores user settings

## Usage

### Accessing Firebase Services

To use Firebase services in your code, import the `firebase_service` module:

```python
from app.services.firebase_service import firebase_service

# Check if Firebase is initialized
if firebase_service.is_initialized():
    # Use Firebase services
    firebase_service.save_document("collection_name", data, document_id)
```

### Session Management

Sessions can be saved and retrieved using the following methods:

```python
# Save a session
firebase_service.save_session(session_id, session_data)

# Get a session
session_data = firebase_service.get_session(session_id)
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

1. Implement more sophisticated security rules for Firestore
2. Add Firebase Authentication integration
3. Implement real-time updates using Firestore listeners
4. Add more comprehensive error handling and retry mechanisms