# NeuroNest-AI Documentation

Welcome to the NeuroNest-AI documentation. This guide will help you understand the architecture, components, and usage of the NeuroNest-AI platform.

## Overview

NeuroNest-AI is an advanced AI agent orchestration platform that enables seamless interaction with multiple specialized AI agents. The platform is designed to be modular, scalable, and secure, with support for multi-device access and offline operation.

## Key Features

- **Multiple AI Agents**: Interact with specialized agents like Thinker, Developer, and more
- **Agent Orchestration**: Intelligent routing of requests to the most appropriate agent
- **Conversation Memory**: Persistent storage of conversations with context awareness
- **Multi-Device Support**: Access your conversations from any device
- **Secure Authentication**: JWT-based authentication with device management
- **Modern Frontend**: Responsive UI built with Next.js and Tailwind CSS
- **Scalable Backend**: FastAPI backend with PostgreSQL and Redis
- **Containerized Deployment**: Easy deployment with Docker and Docker Compose

## Getting Started

- [Installation Guide](installation.md)
- [User Guide](user-guide.md)
- [Developer Guide](developer-guide.md)
- [API Reference](api-reference.md)

## Architecture

The NeuroNest-AI platform follows a modern, modular architecture:

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
├── frontend/                 # Next.js frontend application
│
├── config/                   # Configuration management
│   └── settings.py           # Application settings
│
├── alembic/                  # Database migration tools
```

## Contributing

We welcome contributions to NeuroNest-AI! Please see our [Contributing Guide](contributing.md) for more information.