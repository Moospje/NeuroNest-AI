# Installation Guide

This guide will help you set up NeuroNest-AI on your system.

## Prerequisites

Before installing NeuroNest-AI, make sure you have the following prerequisites:

- Python 3.10 or higher
- Node.js 18 or higher
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (for local development)
- Redis (for local development)

## Installation Options

There are two ways to install and run NeuroNest-AI:

1. **Docker Deployment**: The easiest way to get started
2. **Manual Installation**: For development and customization

## Docker Deployment

The simplest way to deploy NeuroNest-AI is using Docker Compose:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/NeuroNest-AI.git
cd NeuroNest-AI
```

2. Create a `.env` file:

```bash
cp .env.example .env
```

3. Edit the `.env` file with your configuration:

```
# Application settings
PROJECT_NAME=NeuroNest-AI
DEBUG=False

# API settings
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database settings
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@db:5432/neuronest

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# OpenAI settings
OPENAI_API_KEY=your-openai-api-key
```

4. Start the containers:

```bash
docker-compose up -d
```

5. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Installation

For development or customization, you can install NeuroNest-AI manually:

### Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/NeuroNest-AI.git
cd NeuroNest-AI
```

2. Install Poetry:

```bash
pip install poetry
```

3. Install dependencies:

```bash
poetry install
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Edit the `.env` file with your configuration.

6. Run database migrations:

```bash
poetry run alembic upgrade head
```

7. Start the backend server:

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Access the frontend at http://localhost:3000

## Configuration Options

The `.env` file contains various configuration options:

- `PROJECT_NAME`: The name of the project
- `DEBUG`: Enable or disable debug mode
- `SECRET_KEY`: Secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `SQLALCHEMY_DATABASE_URI`: PostgreSQL connection string
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`: Redis configuration
- `OPENAI_API_KEY`: OpenAI API key for AI agents

## Troubleshooting

If you encounter any issues during installation, check the following:

1. Make sure all prerequisites are installed correctly
2. Check the logs for any error messages:
   - Docker: `docker-compose logs`
   - Backend: Check the terminal where you started the backend server
   - Frontend: Check the terminal where you started the frontend server
3. Verify that the database and Redis are running
4. Ensure that the `.env` file contains the correct configuration