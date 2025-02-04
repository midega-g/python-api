# Dockerizing a FastAPI Application

This guide explains how to Dockerize a FastAPI application using **Python 3.11-slim**, **Poetry** for dependency management, and **Docker**. It also covers how to optimize the Dockerfile to copy only specific files and directories, and explains the differences between various Python Docker image variants.

## Key Concepts

### Python Docker Image Variants

Docker provides multiple Python image variants to suit different use cases. Below is an overview of the key variants:

1. **`python:<version>`** (Default Variant)

   - Example: `python:3.12`
   - Full installation of Python with essential system libraries.
   - Suitable for most applications.

2. **`python:<version>-slim`** (Lightweight Variant)

   - Example: `python:3.12-slim`
   - Stripped-down version of the default image with fewer system libraries.
   - Suitable for production environments where size matters.

3. **`python:<version>-alpine`** (Minimalist Variant)

   - Example: `python:3.12-alpine`
   - Based on Alpine Linux, making it extremely lightweight (~5MB base image).
   - Requires manual installation of missing dependencies.
   - Best for small, performance-focused applications.

4. **`python:<version>-buster` / `python:<version>-bullseye` / `python:<version>-bookworm`** (Debian Variants)

   - Example: `python:3.12-bullseye`
   - Based on specific Debian releases:
      - **Buster**: Older, stable version.
      - **Bullseye**: Newer, widely used.
      - **Bookworm**: Latest Debian release.
   - Good balance between size and compatibility.

5. **`python:<version>-windowsservercore`** (Windows Variant)

   - Example: `python:3.12-windowsservercore`
   - Runs on Windows Server Core.
   - Used for Windows-based environments where Linux containers are not feasible.

6. **`python:<version>-onbuild`** (Deprecated)

   - Previously used for auto-building applications but is no longer maintained.

!!! Choosing the Right Variant

Selecting the right Python Docker variant depends on your application's needs. Use `slim` or `alpine` for smaller images, Debian-based for stability, and Windows variants when required. Always consider security, performance, and dependency management when choosing an image.

| Variant | Use Case |
|---------|---------|
| `python:<version>` | General-purpose use |
| `python:<version>-slim` | Reducing image size in production |
| `python:<version>-alpine` | Minimalist and performance-focused setups |
| `python:<version>-buster/bullseye/bookworm` | Debian-based, compatibility-focused |
| `python:<version>-windowsservercore` | Windows-based applications |

### Poetry for Dependency Management

- **Poetry** is a modern dependency management and packaging tool for Python.
- It simplifies dependency resolution, virtual environment management, and packaging.
- Use `poetry install --no-dev` to install only production dependencies in the Docker container.

### Dockerfile Optimization

- Copy only necessary files and directories to reduce image size and improve build efficiency.
- Use multi-stage builds to separate the build environment from the runtime environment.

## Single-Stage DockerFile Build

**Advantages:**

- **Simpler Dockerfile:** Easier to understand and manage.
- **Faster Build Time:** Fewer stages mean quicker builds in simple use cases.

**Disadvantages:**

- **Larger Image Size:** Contains build tools (like `gcc`) and all Poetry files, making it heavier.
- **Security Risks:** Exposes build tools in the runtime environment, increasing potential attack surfaces.

### 1. **Base Image**

   Use `python:3.11-slim` as the base image:

   ```dockerfile
   FROM python:3.11-slim as base
   ```

### 2. **Set Working Directory**

   Set the working directory inside the container:

   ```dockerfile
   WORKDIR /app
   ```

### 3. **Install Poetry**

   Install Poetry in the container:

   ```dockerfile
   RUN pip install poetry
   ```

### 4. **Copy Only Necessary Files**

   Copy only the files required for dependency installation:

   ```dockerfile
   COPY pyproject.toml poetry.lock ./
   ```

### 5. **Install Dependencies**

   Install dependencies using Poetry:

   ```dockerfile
   RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi --no-dev
   ```

- **`virtualenvs.create false`:** This command configures Poetry to **not create virtual environments**. By default, Poetry creates a virtual environment for the project. Setting this to `false` ensures that Poetry installs the dependencies in the system Python environment or the Docker container's environment directly.
- **`--no-root`:** This flag prevents Poetry from installing the project itself (the current project folder) as a package. This is typically used when you only need the dependencies and don't need to install the project as a package.
- **`--no-interaction`:** Prevents Poetry from prompting for user interaction during installation, which is useful for non-interactive environments like Docker builds.
- **`--no-ansi`:** Disables colored output, which can make the build logs more readable.
- **`--only main`:** Skips installing development dependencies, which is commonly done in production environments.

### 6. **Copy Application Code**

   Copy the application code into the container:

   ```dockerfile
   COPY app ./app
   COPY alembic ./alembic
   COPY alembic.ini ./
   ```

### 7. **Run Alembic Migrations**

   Apply database migrations using Alembic:

   ```dockerfile
   RUN poetry run alembic upgrade head
   ```

### 8. **Set the Startup Command**

   Use Gunicorn with Uvicorn workers to serve the FastAPI application:

   ```dockerfile
   CMD ["poetry", "run", "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
   ```

Using `uvicorn --reload` in production is not recommended as it slows down performance and is intended for development, hence the use of gunicorn.

### Full Dockerfile

Check the complete Dockerfile [here](../../Dockerfile)

## Building and Running the Docker Image

### 1. **Build the Docker Image**

   Run the following command to build the Docker image:

   ```bash
   docker build -t fastapi-app .
   ```

   Note that this command will generate an error that requires the input of environment variables and for that docker compose will be useful as continuing to use Dockerfile alone would require us to add the following to the file:

   ```dockerfile
   # Define build-time arguments
   ARG DATABASE_HOSTNAME
   ARG DATABASE_PORT
   ARG DATABASE_PASSWORD
   ARG DATABASE_NAME
   ARG DATABASE_USERNAME
   ARG SECRET_KEY_FASTAPI_AUTH
   ARG ALGORITHM
   ARG ACCESS_TOKEN_EXPIRE_MINUTES

   # Convert ARGs to ENVs
   ENV DATABASE_HOSTNAME=${DATABASE_HOSTNAME}
   ENV DATABASE_PORT=${DATABASE_PORT}
   ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}
   ENV DATABASE_NAME=${DATABASE_NAME}
   ENV DATABASE_USERNAME=${DATABASE_USERNAME}
   ENV SECRET_KEY_FASTAPI_AUTH=${SECRET_KEY_FASTAPI_AUTH}
   ENV ALGORITHM=${ALGORITHM}
   ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
   ```

   Which would then require us to use the following command, passing in the correct values where necessary:

   ```bash
   docker build \
      --build-arg DATABASE_HOSTNAME=your_db_host \
      --build-arg DATABASE_PORT=5432 \
      --build-arg DATABASE_PASSWORD=your_db_password \
      --build-arg DATABASE_NAME=your_db_name \
      --build-arg DATABASE_USERNAME=your_db_user \
      --build-arg SECRET_KEY_FASTAPI_AUTH=your_secret_key \
      --build-arg ALGORITHM=HS256 \
      --build-arg ACCESS_TOKEN_EXPIRE_MINUTES=30 \
      -t fastapi-app .
   ```

### 2. **Run the Docker Container**

   Start the container using the built image:

   ```bash
   docker run -p 8000:8000 fastapi-app
   ```

### 3. **Access the Application**

   Open your browser or use a tool like `curl` to access the FastAPI application:

   ```bash
   curl http://localhost:8000
   ```

## Optimizing the Docker Build

### 1. **Multi-Stage Builds**

   Use multi-stage builds to reduce the final image size:

   ```dockerfile
   # Stage 1: Build environment
   FROM python:3.11-slim as builder

   WORKDIR /app
   RUN pip install poetry
   COPY pyproject.toml poetry.lock ./
   RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi --only main

   # Stage 2: Runtime environment
   FROM python:3.11-slim

   WORKDIR /app
   COPY --from=builder /app /app
   COPY app ./app
   COPY alembic ./alembic
   COPY alembic.ini ./

   RUN poetry run alembic upgrade head
   CMD ["poetry", "run", "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
   ```

#### **Advantages:**

- **Reduced Image Size:** Only the runtime dependencies are included in the final image, minimizing the image size.
- **Isolated Build Environment:** Keeps build tools (like compilers) out of the final image, improving security and reducing attack surfaces.
- **Cleaner and More Secure:** No unnecessary files or build artifacts in the runtime image.

#### **Disadvantages:**

- Slightly more complex Dockerfile due to multiple stages.

### 2. **`.dockerignore` File**

   Create a `.dockerignore` file to exclude unnecessary files from the Docker build context:

   ```dockerignore
   __pycache__
   .git
   .env
   *.pyc
   *.pyo
   *.pyd
   .python-version
   ```

[[TOC]]
