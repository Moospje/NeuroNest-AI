# Architecture Overview

NeuroNest-AI follows a modern, modular architecture designed for scalability, maintainability, and extensibility. This document provides an overview of the system architecture.

## System Components

The NeuroNest-AI system consists of the following main components:

1. **Backend API**: A FastAPI-based REST API that handles requests from clients
2. **Agent System**: A collection of specialized AI agents that process user requests
3. **Database**: A PostgreSQL database for persistent storage
4. **Cache**: A Redis cache for temporary storage and performance optimization
5. **Frontend**: A Next.js-based web application for user interaction

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│  Backend API│────▶│    Agents   │
│  (Next.js)  │◀────│  (FastAPI)  │◀────│             │
└─────────────┘     └─────────────┘     └─────────────┘
                          │ ▲                  │ ▲
                          │ │                  │ │
                          ▼ │                  ▼ │
                    ┌─────────────┐     ┌─────────────┐
                    │  Database   │     │    Cache    │
                    │(PostgreSQL) │     │   (Redis)   │
                    └─────────────┘     └─────────────┘
```

## Backend Architecture

The backend follows a layered architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Service Layer**: Contains business logic
3. **Data Access Layer**: Interacts with the database and cache
4. **Agent Layer**: Manages AI agents and their interactions

### Directory Structure

```
NeuroNest-AI/
│
├── agents/                   # AI agent implementations
│   ├── base_agent.py         # Base agent class
│   ├── thinker_agent.py      # Analytical thinking agent
│   ├── developer_agent.py    # Code and technical agent
│   ├── autogen_agent.py      # AutoGen multi-agent framework
│   └── crewai_agent.py       # CrewAI agent framework
│
├── api/                      # FastAPI routes and endpoints
│   └── routes/
│       ├── auth.py           # Authentication endpoints
│       ├── chat.py           # Conversation and messaging endpoints
│       └── agents.py         # Agent management endpoints
│
├── core/                     # Core system components
│   ├── orchestrator.py       # Agent orchestration logic
│   ├── memory.py             # Conversation memory management
│   └── security.py           # Security utilities
│
├── database/                 # Database models and utilities
│   ├── base.py               # SQLAlchemy base setup
│   ├── models.py             # Database models
│   └── session.py            # Database session management
│
├── config/                   # Configuration management
│   └── settings.py           # Application settings
│
├── alembic/                  # Database migration tools
│
├── main.py                   # Application entry point
```

## Frontend Architecture

The frontend follows a component-based architecture using Next.js and React:

1. **Pages**: Next.js pages that define routes
2. **Components**: Reusable UI components
3. **Hooks**: Custom React hooks for state management and API calls
4. **Store**: Global state management using Zustand
5. **API**: Client-side API utilities for communicating with the backend

### Directory Structure

```
frontend/
│
├── app/                      # Next.js app directory
│   ├── page.tsx              # Home page
│   ├── layout.tsx            # Root layout
│   ├── login/                # Login page
│   ├── register/             # Registration page
│   └── dashboard/            # Dashboard pages
│
├── components/               # React components
│   ├── ui/                   # UI components
│   ├── chat/                 # Chat-related components
│   └── layout/               # Layout components
│
├── lib/                      # Utility functions
│
├── store/                    # State management
│
├── styles/                   # CSS styles
│
├── public/                   # Static assets
│
├── next.config.js            # Next.js configuration
└── tailwind.config.js        # Tailwind CSS configuration
```

## Data Flow

1. **User Request**: The user interacts with the frontend, which sends a request to the backend API
2. **Authentication**: The API authenticates the request using JWT tokens
3. **Request Processing**: The API processes the request and routes it to the appropriate handler
4. **Agent Orchestration**: For chat requests, the orchestrator determines which agent(s) should handle the request
5. **Agent Processing**: The selected agent processes the request and generates a response
6. **Response**: The API returns the response to the frontend, which displays it to the user

## Database Schema

The database schema includes the following main tables:

1. **users**: User accounts and authentication information
2. **devices**: User devices for multi-device support
3. **agents**: Available AI agents and their configurations
4. **conversations**: User conversations
5. **messages**: Individual messages within conversations
6. **logs**: System logs for monitoring and debugging

## Security

NeuroNest-AI implements several security measures:

1. **Authentication**: JWT-based authentication with token expiration
2. **Authorization**: Role-based access control for API endpoints
3. **Password Security**: Bcrypt password hashing
4. **HTTPS**: Secure communication between client and server
5. **Input Validation**: Validation of all user inputs
6. **Rate Limiting**: Protection against brute force attacks

## Deployment

NeuroNest-AI can be deployed using Docker and Docker Compose:

1. **Backend Container**: Runs the FastAPI application
2. **Frontend Container**: Runs the Next.js application
3. **Database Container**: Runs PostgreSQL
4. **Cache Container**: Runs Redis

The system can be deployed to any environment that supports Docker, including:

1. **Local Development**: Docker Compose for local development
2. **Production**: Kubernetes for production deployment
3. **Cloud Providers**: AWS, GCP, Azure, etc.