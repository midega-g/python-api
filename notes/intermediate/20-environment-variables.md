# Environment Variables in FastAPI

## Why Avoid Hardcoding Sensitive Information

- **Security Risks**: Hardcoding database URLs, usernames, and passwords in code exposes sensitive information.
  - Example: Checking code into GitHub can expose credentials to anyone with access.
- **Environment-Specific Issues**: Hardcoded values are tied to a specific environment (e.g., development).
  - In production, the database might be on a different server, requiring code updates.

## Solution: Environment Variables

- **Environment Variables**: Variables configured on a computer that any application can access.
  - Avoid hardcoding sensitive information by storing it in environment variables.
  - Example: Store the database URL in an environment variable named `POSTGRES_URL`.

### Accessing Environment Variables

- **Python Code**: Use the `os` module to access environment variables.

  ```python
  import os
  db_url = os.getenv("POSTGRES_URL")
  print(db_url)
  ```

### Setting Environment Variables

- **Windows**:
  1. Search for "Environment Variables" in the system settings.
  2. Add a new variable under "User Variables" or "System Variables".
  3. Example: Create a variable `MY_DB_URL` with the value `localhost:5432`.
- **Mac/Linux**:
  - Use the terminal to set environment variables.

  ```bash
  export MY_DB_URL="localhost:5432"
  echo $MY_DB_URL
  ```

### Common Issues

- **Windows Terminal**: New environment variables may not be recognized until the terminal is restarted.
- **VS Code on Windows**: Sometimes, VS Code terminals do not recognize newly set environment variables. Restarting VS Code may be necessary.

## Using `.env` Files for Development

- **`.env` File**: A file to store environment variables for development usually located in the root folder of the project
  - Example:

    ```plain text
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_PASSWORD=password123
    DATABASE_NAME=fastapi
    DATABASE_USERNAME=postgres
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

- **Pydantic Validation**: Use the `pydantic` library to validate environment variables, in this case we create a `config.py` file in the `app` folder

  ```python
  from pydantic import BaseSettings

  class Settings(BaseSettings):
      database_hostname: str = "localhost"
      database_port: str = "5432"
      database_password: str
      database_name: str
      database_username: str
      secret_key: str
      algorithm: str
      access_token_expire_minutes: int

      class Config:
          env_file = ".env"

  settings = Settings()
  ```

### Accessing Variables in Code

- **Database Connection**: In the `database.py` file include or update pre-existing code with this

  ```python
   from app.config import settings

   SQLALCHEMY_DATABASE_URL = (
      f"postgresql+psycopg://{settings.DATABASE_USERNAME}:"
      f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:"
      f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
   )
  ```

- **OAuth2 Configuration**:

  ```python
  from config import settings

  SECRET_KEY = settings.secret_key
  ALGORITHM = settings.algorithm
  ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
  ```

### Git Ignore `.env` File

- **`.gitignore`**: Ensure the `.env` file is not checked into Git to avoid exposing sensitive information.

  ```
  .env
  __pycache__/
  venv/
  ```

## Summary

- **Environment Variables**: Essential for managing sensitive information and environment-specific configurations.
- **`.env` Files**: Simplify development by storing environment variables in a file.
- **Pedantic Validation**: Automatically validate and cast environment variables using `pydantic`.
- **Git Ignore**: Never commit `.env` files to version control to protect sensitive data.

[[TOC]]
