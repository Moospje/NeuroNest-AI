# NeuroNest-AI

NeuroNest-AI is an advanced AI agent orchestration platform that enables seamless interaction with multiple specialized AI agents. The platform is designed to be modular, scalable, and secure, with support for multi-device access and offline operation.

## Features

- **Multiple AI Agents**: Interact with specialized agents like Thinker, Developer, and more
- **Agent Orchestration**: Intelligent routing of requests to the most appropriate agent
- **Conversation Memory**: Persistent storage of conversations with context awareness
- **Multi-Device Support**: Access your conversations from any device
- **Secure Authentication**: JWT-based authentication with device management
- **Modern Frontend**: Responsive UI built with Next.js and Tailwind CSS
- **Scalable Backend**: FastAPI backend with PostgreSQL and Redis
- **Containerized Deployment**: Easy deployment with Docker and Docker Compose

## Architecture

The project follows a modern, modular architecture:

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
│
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration for backend
└── pyproject.toml            # Poetry dependency management
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (for local development)
- Redis (for local development)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/NeuroNest-AI.git
cd NeuroNest-AI
```

2. Set up the backend:

```bash
# Install Poetry
pip install poetry

# Install dependencies
poetry install

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
poetry run alembic upgrade head

# Start the backend server
poetry run uvicorn main:app --reload
```

3. Set up the frontend:

```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

To deploy the entire stack using Docker:

```bash
# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Build and start the containers
docker-compose up -d
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.