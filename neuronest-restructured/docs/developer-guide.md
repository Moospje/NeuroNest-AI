# Developer Guide

This guide is intended for developers who want to extend, customize, or contribute to NeuroNest-AI. It covers the development environment setup, architecture, and guidelines for contributing to the project.

## Development Environment Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- Node.js 18 or higher
- Docker and Docker Compose
- PostgreSQL
- Redis
- Git

### Setting Up the Development Environment

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
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Set up the frontend:

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

NeuroNest-AI follows a modular architecture:

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

## Backend Development

### Adding a New API Endpoint

To add a new API endpoint:

1. Create a new route in the appropriate file in `api/routes/`
2. Define the request and response models using Pydantic
3. Implement the route handler function
4. Add the route to the API router in `api/__init__.py`

Example:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import User
from core.security import get_current_user

router = APIRouter()

@router.get("/example")
def example_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Example endpoint.
    """
    return {"message": "This is an example endpoint"}
```

### Creating a New Agent

To create a new agent:

1. Create a new file in the `agents/` directory
2. Define a class that inherits from `BaseAgent`
3. Implement the `run` method
4. Register the agent in the database

Example:

```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    """
    A custom agent that does something specific.
    """
    
    def __init__(self):
        super().__init__(
            name="MyCustom",
            description="A custom agent that does something specific."
        )
    
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the agent on the given input.
        """
        # Implement your agent logic here
        return f"Custom agent response to: {input_text}"
```

### Database Migrations

When you make changes to the database models, you need to create a migration:

```bash
# Generate a new migration script
poetry run alembic revision --autogenerate -m "Description of the changes"

# Apply the migration
poetry run alembic upgrade head
```

## Frontend Development

### Adding a New Page

To add a new page:

1. Create a new directory in `frontend/app/`
2. Create a `page.tsx` file in the directory
3. Implement the page component
4. Add navigation to the page in the appropriate components

Example:

```tsx
// frontend/app/example/page.tsx
export default function ExamplePage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Example Page</h1>
      <p>This is an example page.</p>
    </div>
  );
}
```

### Creating a New Component

To create a new component:

1. Create a new file in the appropriate directory in `frontend/components/`
2. Implement the component
3. Export the component

Example:

```tsx
// frontend/components/ui/ExampleComponent.tsx
import { ReactNode } from 'react';

interface ExampleComponentProps {
  title: string;
  children: ReactNode;
}

export function ExampleComponent({ title, children }: ExampleComponentProps) {
  return (
    <div className="border rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-2">{title}</h2>
      <div>{children}</div>
    </div>
  );
}
```

### Adding a New API Client Function

To add a new API client function:

1. Add the function to the appropriate file in `frontend/lib/api/`
2. Implement the function using Axios

Example:

```tsx
// frontend/lib/api/example.ts
import api from './api';

export async function getExampleData() {
  const response = await api.get('/api/v1/example');
  return response.data;
}
```

## Testing

### Backend Testing

To run backend tests:

```bash
poetry run pytest
```

To write a new test:

1. Create a new file in the `tests/` directory
2. Implement the test functions
3. Run the tests

Example:

```python
# tests/test_example.py
def test_example(client):
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    assert "message" in response.json()
```

### Frontend Testing

To run frontend tests:

```bash
cd frontend
npm test
```

To write a new test:

1. Create a new file with the `.test.tsx` extension next to the component you want to test
2. Implement the test functions
3. Run the tests

Example:

```tsx
// frontend/components/ui/ExampleComponent.test.tsx
import { render, screen } from '@testing-library/react';
import { ExampleComponent } from './ExampleComponent';

describe('ExampleComponent', () => {
  it('renders the title and children', () => {
    render(
      <ExampleComponent title="Test Title">
        <p>Test Content</p>
      </ExampleComponent>
    );
    
    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });
});
```

## Docker Development

To develop using Docker:

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

## Continuous Integration

NeuroNest-AI uses GitHub Actions for continuous integration. The CI pipeline runs on every push and pull request, and includes:

1. Linting and code formatting checks
2. Backend tests
3. Frontend tests
4. Build checks

## Deployment

To deploy NeuroNest-AI:

1. Build the Docker images:

```bash
docker-compose build
```

2. Push the images to a registry:

```bash
docker-compose push
```

3. Deploy to your server:

```bash
# On your server
docker-compose pull
docker-compose up -d
```

## Contributing Guidelines

When contributing to NeuroNest-AI, please follow these guidelines:

1. **Code Style**: Follow the established code style
   - Backend: Use Black for formatting
   - Frontend: Use Prettier for formatting

2. **Commit Messages**: Write clear, descriptive commit messages
   - Use the imperative mood ("Add feature" not "Added feature")
   - Reference issue numbers when applicable

3. **Pull Requests**: Create a pull request for each feature or bug fix
   - Provide a clear description of the changes
   - Include tests for new features
   - Ensure all tests pass

4. **Documentation**: Update documentation for new features
   - Add inline code comments
   - Update relevant documentation files

5. **Testing**: Write tests for new features and bug fixes
   - Backend: Use pytest
   - Frontend: Use Jest and React Testing Library

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Check that PostgreSQL is running
   - Verify the database connection string in `.env`

2. **Redis Connection Issues**:
   - Check that Redis is running
   - Verify the Redis connection settings in `.env`

3. **Frontend Build Issues**:
   - Clear the Next.js cache: `rm -rf frontend/.next`
   - Reinstall dependencies: `cd frontend && rm -rf node_modules && npm install`

4. **Backend Dependency Issues**:
   - Update Poetry: `poetry update`
   - Recreate the virtual environment: `poetry env remove python && poetry install`

### Getting Help

If you need help with development:

- Check the existing documentation
- Look for similar issues in the GitHub repository
- Ask for help in the community Discord server
- Open an issue on GitHub