#!/bin/bash

# Exit on error
set -e

# Change to project root directory
cd "$(dirname "$0")/.."

# Create initial migration
echo "Creating initial migration..."
alembic revision --autogenerate -m "initial"

# Apply migrations
echo "Applying migrations..."
alembic upgrade head

echo "Database migrations completed successfully!"