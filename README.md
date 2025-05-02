# NeuroNest-AI

![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![CI/CD](https://github.com/Moospje/NeuroNest-AI/workflows/NeuroNest%20AI%20CI/CD/badge.svg)

NeuroNest-AI is a comprehensive AI platform that provides an integrated environment for developing and running intelligent agents with full support for Arabic language and dialects. The platform features a modern FastAPI backend with PostgreSQL database and a React/Next.js frontend.

## Features

- **Modern Architecture**: FastAPI backend with PostgreSQL database and React/Next.js frontend.
- **JWT Authentication**: Secure authentication with refresh tokens and device management.
- **Redis Integration**: Token storage and session management with Redis.
- **Agent Orchestration**: Dynamic routing of requests to appropriate AI agents.
- **Conversation Management**: Persistent conversation history with agent context.
- **Multi-device Support**: Login from multiple devices with secure token management.
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions.
- **Docker Support**: Containerized deployment for all services.
- **Arabic Dialect Support**: Interface for selecting specific Arabic dialects for speech recognition.
- **Runtime & Preview Engine**: Real execution environment for created projects (Web Apps, Python Apps, etc.).

## Project Structure

```
NeuroNest-AI/
├── frontend/                # React/Next.js frontend
│   ├── public/              # Static assets
│   └── src/                 # Source code
│       ├── components/      # React components
│       ├── contexts/        # React contexts
│       ├── pages/           # Next.js pages
│       └── services/        # API services
├── backend-express/         # Legacy Node.js/Express backend
│   ├── routes/              # API routes
│   ├── controllers/         # Request handlers
│   ├── services/            # Business logic
│   └── middleware/          # Express middleware
├── api/                     # FastAPI backend
│   ├── main.py              # Main application entry point
│   └── v1/                  # API version 1
│       ├── api.py           # API router
│       └── endpoints/       # API endpoints
├── agents/                  # AI agents implementation
│   ├── base.py              # Base agent class
│   └── openai_agent.py      # OpenAI agent implementation
├── core/                    # Core functionality
│   ├── security.py          # Authentication and security
│   └── deps.py              # Dependency injection
├── database/                # Database models and session
│   ├── models.py            # SQLAlchemy models
│   ├── session.py           # Database session
│   └── base.py              # Base model class
├── config/                  # Configuration
│   └── settings.py          # Application settings
├── scripts/                 # Utility scripts
├── CHANGELOG.md             # Version history
├── VERSIONING_GUIDE.md      # Versioning guidelines
├── DOCUMENTATION_GUIDE.md   # Documentation guidelines
└── OVERVIEW.md              # Project overview
```

## Getting Started

### Prerequisites

- Node.js (v18 or later) for frontend
- Python (v3.10 or later) for FastAPI backend
- Docker and Docker Compose (recommended)
- PostgreSQL (if not using Docker)
- Redis (if not using Docker)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Moospje/NeuroNest-AI.git
   cd NeuroNest-AI
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Install FastAPI backend dependencies:
   ```bash
   # From the root directory
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env.local` in the frontend directory
   - Create a `.env` file in the root directory for FastAPI backend with the following variables:
     ```
     # Database
     POSTGRES_SERVER=localhost
     POSTGRES_USER=nnuser
     POSTGRES_PASSWORD=nnpass
     POSTGRES_DB=nndb
     POSTGRES_PORT=5432
     
     # Redis
     REDIS_HOST=localhost
     REDIS_PORT=6379
     REDIS_DB=0
     REDIS_PASSWORD=
     
     # Security
     SECRET_KEY=your-secret-key
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     JWT_ALGORITHM=HS256
     
     # API
     API_V1_STR=/api/v1
     ```

5. Run database migrations:
   ```bash
   # From the root directory
   alembic upgrade head
   ```

6. Start the development servers using Docker Compose:
   ```bash
   docker-compose up
   ```

   Or start the services individually:
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d db redis
   
   # Frontend
   cd frontend
   npm run dev
   
   # FastAPI backend
   cd ..
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Testing

Run the automated tests for the backend:

```bash
# From the root directory
pytest
```

Run the frontend tests:

```bash
cd frontend
npm test
```

## Documentation

- [Project Overview](OVERVIEW.md): General information about the project structure and components.
- [Versioning Guide](VERSIONING_GUIDE.md): Guidelines for versioning the project.
- [Documentation Guide](DOCUMENTATION_GUIDE.md): Guidelines for documenting the project.
- [Changelog](CHANGELOG.md): Version history and changes.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the foundation models
- OpenRouter for API integration
- Firebase and Supabase for backend services
