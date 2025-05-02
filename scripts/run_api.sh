#!/bin/bash

# Exit on error
set -e

# Change to project root directory
cd "$(dirname "$0")/.."

# Run the FastAPI application
uvicorn test_main:app --host 0.0.0.0 --port 8000 --reload