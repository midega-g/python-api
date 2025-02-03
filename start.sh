#!/bin/bash
# Apply Alembic migrations
alembic upgrade head

# Use Render's provided PORT if available, otherwise default to 8000
PORT=${PORT:-8000}

# Start the FastAPI application with the selected port
uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
