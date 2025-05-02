# Contributing to NeuroNest-AI

Thank you for your interest in contributing to NeuroNest-AI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a healthy and welcoming community.

## How to Contribute

There are many ways to contribute to NeuroNest-AI:

1. **Report bugs**: If you find a bug, please report it by creating an issue on GitHub.
2. **Suggest features**: If you have an idea for a new feature, please create an issue on GitHub.
3. **Improve documentation**: Help us improve the documentation by fixing typos, adding examples, or clarifying explanations.
4. **Write code**: Contribute bug fixes or new features by submitting pull requests.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- Node.js 18 or higher
- Docker and Docker Compose
- PostgreSQL
- Redis
- Git

### Setting Up the Development Environment

1. Fork the repository on GitHub.
2. Clone your fork locally:

```bash
git clone https://github.com/yourusername/NeuroNest-AI.git
cd NeuroNest-AI
```

3. Set up the backend:

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

4. Set up the frontend:

```bash
cd frontend
npm install
npm run dev
```

## Development Workflow

1. Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:

```bash
git add .
git commit -m "Add your feature or fix"
```

3. Push your changes to your fork:

```bash
git push origin feature/your-feature-name
```

4. Create a pull request on GitHub.

## Pull Request Guidelines

When submitting a pull request:

1. **Keep it focused**: Each pull request should address a single concern.
2. **Write tests**: Add tests for new features or bug fixes.
3. **Update documentation**: Update the documentation to reflect your changes.
4. **Follow code style**: Ensure your code follows the project's code style.
5. **Write a good description**: Explain what your pull request does and why it's needed.

## Code Style

### Backend (Python)

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import sorting
- Use type hints

### Frontend (TypeScript/React)

- Follow the Airbnb JavaScript Style Guide
- Use Prettier for code formatting
- Use ESLint for linting
- Use TypeScript for type safety

## Testing

### Backend Testing

Run backend tests with pytest:

```bash
poetry run pytest
```

### Frontend Testing

Run frontend tests with Jest:

```bash
cd frontend
npm test
```

## Documentation

Documentation is written in Markdown and built with MkDocs. To build and preview the documentation:

```bash
# Install MkDocs and required plugins
pip install mkdocs mkdocs-material mkdocstrings

# Build and serve the documentation
mkdocs serve
```

## Issue Guidelines

When creating an issue:

1. **Use a clear title**: The title should concisely describe the issue.
2. **Provide a detailed description**: Explain the issue in detail, including steps to reproduce if it's a bug.
3. **Include relevant information**: Include your environment details, error messages, and screenshots if applicable.
4. **Use issue templates**: Use the provided issue templates when available.

## Feature Requests

When requesting a feature:

1. **Describe the problem**: Explain the problem you're trying to solve.
2. **Suggest a solution**: If you have a solution in mind, describe it.
3. **Provide examples**: Include examples of how the feature would be used.
4. **Explain the benefits**: Explain why this feature would be valuable to users.

## Bug Reports

When reporting a bug:

1. **Describe the bug**: Provide a clear description of the bug.
2. **Steps to reproduce**: List the steps to reproduce the bug.
3. **Expected behavior**: Describe what you expected to happen.
4. **Actual behavior**: Describe what actually happened.
5. **Environment**: Include details about your environment (OS, browser, etc.).
6. **Screenshots**: Include screenshots if applicable.
7. **Additional context**: Add any other context about the problem.

## Review Process

All pull requests will be reviewed by the project maintainers. The review process includes:

1. **Code review**: The code will be reviewed for quality, style, and correctness.
2. **Test verification**: The tests will be run to ensure they pass.
3. **Documentation review**: The documentation will be reviewed for completeness and clarity.
4. **Merge decision**: The pull request will be merged if it meets all requirements.

## Community

Join our community to get help, share ideas, and collaborate:

- **Discord**: Join our [Discord server](https://discord.gg/neuronest-ai)
- **GitHub Discussions**: Participate in [GitHub Discussions](https://github.com/yourusername/NeuroNest-AI/discussions)
- **Twitter**: Follow us on [Twitter](https://twitter.com/neuronest_ai)

## License

By contributing to NeuroNest-AI, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).