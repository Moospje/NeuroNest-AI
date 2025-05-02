# API Reference

This document provides a reference for the NeuroNest-AI API endpoints.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

Most endpoints require authentication. To authenticate, include an `Authorization` header with a Bearer token:

```
Authorization: Bearer <access_token>
```

You can obtain an access token by logging in with the `/api/v1/auth/login` endpoint.

## Endpoints

### Authentication

#### Register a new user

```
POST /api/v1/auth/register
```

Request body:

```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password"
}
```

Response:

```json
{
  "id": "user_id",
  "email": "user@example.com",
  "username": "username",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Login

```
POST /api/v1/auth/login
```

Request body (form data):

```
username=username&password=password
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "device_id": "device_id"
}
```

#### Get current user

```
GET /api/v1/auth/me
```

Response:

```json
{
  "id": "user_id",
  "email": "user@example.com",
  "username": "username",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Conversations

#### List conversations

```
GET /api/v1/conversations
```

Response:

```json
[
  {
    "id": "conversation_id",
    "title": "Conversation Title",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "message_count": 10
  }
]
```

#### Get conversation

```
GET /api/v1/conversations/{conversation_id}
```

Response:

```json
{
  "id": "conversation_id",
  "title": "Conversation Title",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "messages": [
    {
      "id": "message_id",
      "content": "Hello, how can I help you?",
      "role": "assistant",
      "created_at": "2023-01-01T00:00:00Z",
      "agent": "thinker"
    },
    {
      "id": "message_id",
      "content": "I need help with a programming problem.",
      "role": "user",
      "created_at": "2023-01-01T00:00:01Z"
    }
  ]
}
```

#### Create conversation

```
POST /api/v1/conversations
```

Request body:

```json
{
  "title": "Conversation Title"
}
```

Response:

```json
{
  "id": "conversation_id",
  "title": "Conversation Title",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "messages": []
}
```

#### Delete conversation

```
DELETE /api/v1/conversations/{conversation_id}
```

Response:

```json
{
  "message": "Conversation deleted successfully"
}
```

### Messages

#### Send message

```
POST /api/v1/conversations/{conversation_id}/messages
```

Request body:

```json
{
  "content": "I need help with a programming problem.",
  "role": "user"
}
```

Response:

```json
{
  "id": "message_id",
  "content": "I need help with a programming problem.",
  "role": "user",
  "created_at": "2023-01-01T00:00:00Z",
  "conversation_id": "conversation_id"
}
```

#### Get agent response

```
POST /api/v1/chat
```

Request body:

```json
{
  "message": "I need help with a programming problem.",
  "conversation_id": "conversation_id",
  "agent": "developer"  // Optional, if not provided, the orchestrator will select the appropriate agent
}
```

Response:

```json
{
  "response": "I'd be happy to help with your programming problem. What language are you using and what's the issue you're facing?",
  "agent": "developer",
  "conversation_id": "conversation_id",
  "message_id": "message_id"
}
```

### Agents

#### List available agents

```
GET /api/v1/agents
```

Response:

```json
[
  {
    "id": "thinker",
    "name": "Thinker Agent",
    "description": "Analytical thinking and problem-solving agent",
    "capabilities": ["analysis", "reasoning", "problem-solving"]
  },
  {
    "id": "developer",
    "name": "Developer Agent",
    "description": "Code and technical problem-solving agent",
    "capabilities": ["coding", "debugging", "technical-explanation"]
  }
]
```

#### Get agent details

```
GET /api/v1/agents/{agent_id}
```

Response:

```json
{
  "id": "developer",
  "name": "Developer Agent",
  "description": "Code and technical problem-solving agent",
  "capabilities": ["coding", "debugging", "technical-explanation"],
  "examples": [
    "How do I implement a binary search in Python?",
    "Debug this JavaScript code for me",
    "Explain how Docker containers work"
  ]
}
```

## WebSocket API

NeuroNest-AI also provides a WebSocket API for real-time communication.

### Connect to WebSocket

```
WebSocket: /ws/chat/{conversation_id}
```

Authentication is done by including the access token as a query parameter:

```
/ws/chat/{conversation_id}?token={access_token}
```

### WebSocket Messages

#### Send a message

```json
{
  "type": "message",
  "content": "I need help with a programming problem.",
  "conversation_id": "conversation_id"
}
```

#### Receive a message

```json
{
  "type": "message",
  "content": "I'd be happy to help with your programming problem. What language are you using and what's the issue you're facing?",
  "role": "assistant",
  "agent": "developer",
  "conversation_id": "conversation_id",
  "message_id": "message_id",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Stream a response

```json
{
  "type": "stream",
  "content": "I'd be happy to help",
  "conversation_id": "conversation_id",
  "message_id": "message_id",
  "done": false
}
```

```json
{
  "type": "stream",
  "content": " with your programming problem.",
  "conversation_id": "conversation_id",
  "message_id": "message_id",
  "done": false
}
```

```json
{
  "type": "stream",
  "content": " What language are you using and what's the issue you're facing?",
  "conversation_id": "conversation_id",
  "message_id": "message_id",
  "done": true,
  "agent": "developer",
  "created_at": "2023-01-01T00:00:00Z"
}
```