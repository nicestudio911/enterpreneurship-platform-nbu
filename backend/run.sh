#!/bin/bash
# Script to run the backend with venv

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Set environment variables if .env exists in project root
if [ -f "../.env" ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Set default database URL if not set
export DATABASE_URL=${DATABASE_URL:-sqlite:///./data/app.db}

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

