# Use Python 3.11 slim as the base image
FROM python:3.11-slim AS base

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi --only main

# Copy the application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# Start the FastAPI application
CMD ["poetry", "run", "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
