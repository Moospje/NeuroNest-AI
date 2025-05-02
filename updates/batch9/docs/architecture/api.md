# API Architecture

NeuroNest-AI uses FastAPI to provide a modern, high-performance API. This document describes the API architecture, endpoints, and authentication system.

## API Structure

The API follows a RESTful design with versioned endpoints. All endpoints are prefixed with `/api/v1`.

### Directory Structure

```
api/
├── __init__.py               # API router initialization
└── routes/
    ├── __init__.py           # Routes initialization
    ├── auth.py               # Authentication endpoints
    ├── chat.py               # Conversation and messaging endpoints
    └── agents.py             # Agent management endpoints
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register`: Register a new user
- `POST /api/v1/auth/login`: Login and get access token
- `GET /api/v1/auth/me`: Get current user information
- `POST /api/v1/auth/refresh`: Refresh access token
- `POST /api/v1/auth/logout`: Logout and invalidate token

### Conversations

- `GET /api/v1/conversations`: List user conversations
- `POST /api/v1/conversations`: Create a new conversation
- `GET /api/v1/conversations/{conversation_id}`: Get conversation details
- `PUT /api/v1/conversations/{conversation_id}`: Update conversation
- `DELETE /api/v1/conversations/{conversation_id}`: Delete conversation

### Messages

- `GET /api/v1/conversations/{conversation_id}/messages`: List messages in a conversation
- `POST /api/v1/conversations/{conversation_id}/messages`: Add a message to a conversation

### Chat

- `POST /api/v1/chat`: Send a message to an agent and get a response
- `WebSocket /api/v1/ws/chat/{conversation_id}`: Real-time chat with agents

### Agents

- `GET /api/v1/agents`: List available agents
- `GET /api/v1/agents/{agent_id}`: Get agent details

## Authentication System

NeuroNest-AI uses JWT (JSON Web Tokens) for authentication. The authentication flow is as follows:

1. **Registration**: User registers with email, username, and password
2. **Login**: User logs in with username/email and password, receives an access token
3. **Authentication**: User includes the access token in the `Authorization` header for subsequent requests
4. **Refresh**: User can refresh the access token before it expires
5. **Logout**: User can invalidate the access token

### JWT Token

The JWT token contains the following claims:

- `sub`: Subject (user ID)
- `exp`: Expiration time
- `iat`: Issued at time
- `jti`: JWT ID (unique identifier for the token)

### Device-Based Authentication

NeuroNest-AI supports multi-device authentication. Each device receives a unique device ID, which is associated with the user account. This allows users to:

1. Log in from multiple devices simultaneously
2. Manage their devices (view, rename, remove)
3. Maintain separate sessions for each device

## API Implementation

### Route Handlers

Route handlers are implemented using FastAPI's dependency injection system. Here's an example of a route handler:

```python
@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message to an agent and get a response.
    """
    # Get the conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Process the message
    orchestrator = get_orchestrator()
    result = orchestrator.process_message(
        message=request.message,
        conversation_id=str(conversation.id),
        user_id=str(current_user.id),
        agent_name=request.agent
    )
    
    # Store the user message
    memory = Memory(db)
    user_message = memory.add_message(
        conversation_id=str(conversation.id),
        content=request.message,
        role="user"
    )
    
    # Store the agent response
    agent_id = None
    if result["agent"]:
        agent = db.query(Agent).filter(Agent.name == result["agent"]).first()
        if agent:
            agent_id = agent.id
    
    agent_message = memory.add_message(
        conversation_id=str(conversation.id),
        content=result["response"],
        role="assistant",
        agent_id=agent_id
    )
    
    return {
        "response": result["response"],
        "agent": result["agent"],
        "conversation_id": str(conversation.id),
        "message_id": str(agent_message.id)
    }
```

### WebSocket Support

NeuroNest-AI supports real-time communication using WebSockets. The WebSocket endpoint is implemented as follows:

```python
@router.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: str,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Real-time chat with agents.
    """
    # Authenticate the user
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            await websocket.close(code=1008, reason="Invalid authentication token")
            return
    except JWTError:
        await websocket.close(code=1008, reason="Invalid authentication token")
        return
    
    # Get the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=1008, reason="User not found")
        return
    
    # Get the conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()
    
    if not conversation:
        await websocket.close(code=1008, reason="Conversation not found")
        return
    
    # Accept the connection
    await websocket.accept()
    
    # Handle messages
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            
            # Process the message
            orchestrator = get_orchestrator()
            result = orchestrator.process_message(
                message=data["content"],
                conversation_id=str(conversation.id),
                user_id=str(user.id),
                agent_name=data.get("agent")
            )
            
            # Store the user message
            memory = Memory(db)
            user_message = memory.add_message(
                conversation_id=str(conversation.id),
                content=data["content"],
                role="user"
            )
            
            # Store the agent response
            agent_id = None
            if result["agent"]:
                agent = db.query(Agent).filter(Agent.name == result["agent"]).first()
                if agent:
                    agent_id = agent.id
            
            agent_message = memory.add_message(
                conversation_id=str(conversation.id),
                content=result["response"],
                role="assistant",
                agent_id=agent_id
            )
            
            # Send response
            await websocket.send_json({
                "type": "message",
                "content": result["response"],
                "role": "assistant",
                "agent": result["agent"],
                "conversation_id": str(conversation.id),
                "message_id": str(agent_message.id),
                "created_at": agent_message.created_at.isoformat()
            })
    except WebSocketDisconnect:
        # Handle disconnection
        pass
```

## API Documentation

NeuroNest-AI provides automatic API documentation using FastAPI's built-in support for OpenAPI and Swagger UI. The documentation is available at:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Error Handling

NeuroNest-AI uses FastAPI's exception handling system to provide consistent error responses. Common HTTP status codes include:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Rate Limiting

NeuroNest-AI implements rate limiting to prevent abuse. Rate limits are applied to:

- Authentication endpoints (to prevent brute force attacks)
- Chat endpoints (to prevent excessive usage)

## CORS Configuration

NeuroNest-AI configures CORS (Cross-Origin Resource Sharing) to allow requests from the frontend application:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Best Practices

When working with the API:

1. **Use Dependency Injection**: Use FastAPI's dependency injection system for common functionality
2. **Validate Input**: Use Pydantic models to validate request data
3. **Document Endpoints**: Provide clear documentation for all endpoints
4. **Handle Errors**: Return appropriate status codes and error messages
5. **Use Async**: Use async/await for I/O-bound operations
6. **Test Endpoints**: Write tests for all endpoints