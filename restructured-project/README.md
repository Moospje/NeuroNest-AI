# NeuroNest-AI

<div align="center">
  <img src="https://via.placeholder.com/200x200?text=NeuroNest-AI" alt="NeuroNest-AI Logo" width="200" height="200">
  <h3>Advanced AI Agent Orchestration Platform</h3>
</div>

NeuroNest-AI is an advanced AI agent orchestration platform that enables seamless interaction with multiple specialized AI agents. The platform is designed to be modular, scalable, and secure, with support for multi-device access and offline operation.

## ✨ Features

- **🤖 Multiple AI Agents**: Interact with specialized agents like Thinker, Developer, AutoGen, and CrewAI
- **🔄 Agent Orchestration**: Intelligent routing of requests to the most appropriate agent
- **🧠 Conversation Memory**: Persistent storage of conversations with context awareness
- **📱 Multi-Device Support**: Access your conversations from any device with secure synchronization
- **🔒 Secure Authentication**: JWT-based authentication with device management
- **💻 Modern Frontend**: Responsive UI built with Next.js and Tailwind CSS
- **⚡ Scalable Backend**: FastAPI backend with PostgreSQL and Redis
- **🐳 Containerized Deployment**: Easy deployment with Docker and Docker Compose

## 🏗️ Architecture

The project follows a modern, modular architecture designed for scalability and maintainability:

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
│   ├── app/                  # Next.js app directory
│   │   ├── components/       # React components
│   │   ├── lib/              # Utility functions
│   │   ├── store/            # State management
│   │   └── ...               # Pages and layouts
│   ├── public/               # Static assets
│   └── ...                   # Configuration files
│
├── config/                   # Configuration management
│   └── settings.py           # Application settings
│
├── docs/                     # Documentation
│   ├── architecture/         # Architecture documentation
│   └── ...                   # User and developer guides
│
├── tests/                    # Test suite
│   ├── conftest.py           # Test configuration
│   └── ...                   # Test modules
│
├── alembic/                  # Database migration tools
│
├── scripts/                  # Utility scripts
│
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration for backend
└── pyproject.toml            # Poetry dependency management
```

### System Components

<div align="center">
  <img src="https://via.placeholder.com/800x400?text=NeuroNest-AI+Architecture" alt="NeuroNest-AI Architecture" width="800">
</div>

The system consists of several key components that work together:

1. **Frontend**: Next.js application that provides the user interface
2. **Backend API**: FastAPI application that handles requests from the frontend
3. **Agent System**: Collection of AI agents that process user requests
4. **Database**: PostgreSQL database for persistent storage
5. **Cache**: Redis cache for temporary storage and performance optimization

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** - For the backend application
- **Node.js 18+** - For the frontend application
- **Docker & Docker Compose** - For containerized deployment
- **PostgreSQL** - For local development (optional if using Docker)
- **Redis** - For local development (optional if using Docker)

### Installation

#### Option 1: Local Development

1. **Clone the repository**:

```bash
git clone https://github.com/kaohq8/NeuroNest-AI.git
cd NeuroNest-AI
```

2. **Set up the backend**:

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
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **Set up the frontend**:

```bash
cd frontend
npm install
npm run dev
```

#### Option 2: Docker Deployment

To deploy the entire stack using Docker:

```bash
# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Build and start the containers
docker-compose up -d
```

### Mobile Access

You can access NeuroNest-AI from your mobile device:

1. Make sure your computer and mobile device are on the same network
2. Find your computer's IP address (e.g., 192.168.1.100)
3. Access the application from your mobile browser at `http://192.168.1.100:3000`

### Desktop Application

To run NeuroNest-AI as a desktop application:

1. Install Electron wrapper (from the project root):

```bash
cd desktop
npm install
npm start
```

This will launch the application in a desktop window with additional native features.

## 📚 API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

The API provides endpoints for:

- User authentication and device management
- Conversation and message handling
- Agent interaction and management

## 🧠 AI Agents

NeuroNest-AI includes several specialized AI agents:

### Thinker Agent

The Thinker Agent specializes in analytical thinking and problem-solving. It's designed to:

- Break down complex problems into manageable parts
- Provide step-by-step reasoning
- Analyze situations from multiple perspectives
- Generate creative solutions

### Developer Agent

The Developer Agent specializes in code and technical problem-solving. It can:

- Write and debug code in various programming languages
- Explain technical concepts
- Review and optimize code
- Provide guidance on software architecture and design patterns

### AutoGen Agent

The AutoGen Agent uses the AutoGen framework to coordinate multiple AI agents. It can:

- Orchestrate conversations between specialized agents
- Solve complex problems that require multiple perspectives
- Manage multi-step workflows
- Provide comprehensive solutions by combining different agent capabilities

### CrewAI Agent

The CrewAI Agent uses the CrewAI framework to create and manage a crew of specialized agents. It can:

- Assign roles to different agents based on their capabilities
- Coordinate complex tasks with multiple steps
- Manage dependencies between agent tasks
- Provide a unified interface for interacting with multiple agents

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For more details, see our [Contributing Guide](docs/contributing.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you need help with NeuroNest-AI:

- Check the [documentation](docs/index.md)
- Open an [issue](https://github.com/kaohq8/NeuroNest-AI/issues)
- Contact the maintainers at support@neuronest-ai.com