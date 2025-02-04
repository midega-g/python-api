# Docker Compose for FastAPI and PostgreSQL

Docker Compose simplifies the management of multi-container applications by defining configurations in a single YAML file. In this setup, we will focus on two services:

1. **FastAPI Service** – The backend application running with Gunicorn.
2. **PostgreSQL Service** – The database for storing application data.

This guide explains each section of the `docker-compose-dev.yml` file, detailing what each line does, followed by a complete YAML file and useful Docker commands.

## Docker Compose Configuration File

### 1. Specify Docker Compose Version

```yaml
version: "3.8"
```

- Specifies the Docker Compose version.
- Using version `3.8` ensures compatibility with modern Docker features.

### 2. Define Services (Containers)

a) **FastAPI Application Service**

```yaml
services:
  api:
    build: .  # Uses the Dockerfile in the current directory
    container_name: fastapi_app
    ports:
      - "8000:8000"  # Maps port 8000 on the host to 8000 in the container
    depends_on:
      - postgres  # Ensures the database starts before the API
    environment:
      - DATABASE_HOST=postgres
      - DATABASE_USER=admin
      - DATABASE_PASSWORD=securepassword
      - DATABASE_NAME=fastapi_db
    volumes:
      - .:/app  # Syncs local app directory with container app directory
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - fastapi_network
```

- `build: .` – Uses the Dockerfile in the project directory to build the API image.
- `container_name: fastapi_app` – Assigns a custom name to the container.
- `ports:` – Maps the container’s port 8000 to the host’s port 8000.
- `depends_on:` – Ensures that the PostgreSQL database starts before the API service.
- `environment:` – Passes environment variables to configure the database connection.
- `volumes:` – Mounts everything thing in the local directory (but not included in `.dockerignore` file) inside the container to reflect code changes. If you want only changes in a particular directory, say `app`, to be reflected, then use `./app` instead of `.`
- `command:` – Uses Uvicorn workers to run the FastAPI application. Since this is a development environment, we use it with the reload flag to enable automatic reloading when changes are made in our code
- `networks:` – Connects the container to a custom Docker network.

b) **PostgreSQL Database Service**

```yaml
  postgres:
    image: postgres:14
    container_name: fastapi_db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: securepassword
      POSTGRES_DB: fastapi_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - fastapi_network
```

- `image: postgres:14` – Uses the official PostgreSQL image (version 14).
- `container_name: fastapi_db` – Assigns a custom name to the PostgreSQL container.
- `environment:` – Sets credentials and the database name.
- `volumes:` – Persists PostgreSQL data using a named volume.
- `networks:` – Connects the database container to the same network as the API.

### 3. Define Named Volumes

- Data inside a container is lost when it shuts down.
- Use named volumes to persist data:
- Named volumes allow multiple containers to access stored data.

```yaml
volumes:
  postgres_data:
```

- `postgres_data:` – A named volume that persists PostgreSQL data across container restarts.

### 4. (Optional) Define a Network

- If not explicitly defined, Docker Compose creates a custom network with the naming convention of:

  ```plaintext
  project_directory_default
  ```

- Containers can communicate using service names which in this case is `postgres`:

  ```yaml
  DATABASE_HOST: postgres
  ```

- To explicitly define a network ensure you include the following:

  ```yaml
  api:
    # other commands goes here
    networks:
      - fastapi_network

  postgres:
    # other commands goes here
    networks:
      - fastapi_network

  networks:
    fastapi_network:
      driver: bridge
  ```

- This creates a custom bridge network (`fastapi_network`) to enable communication between services.

### **5. (extras) Naming Convention in Docker Compose**

- If we don't give a container name, the naming convention would follow the pattern:

  ```plaintext
  project_directory_service_name_instance_number
  ```

  For example if the project directory was `fastapi` and the service name was `api`, the output would be:

  ```plaintext
  fastapi_api_1
  ```

- If four instances of the same service were running, they would be named:

  ```plaintext
  fastapi_api_1, fastapi_api_2, fastapi_api_3, fastapi_api_4
  ```

## Complete `docker-compose-dev.yml` File

Check the complete Docker Compose file [here](../../docker-compose-dev.yml)

## Useful Docker Compose Commands

Note, depending on your configuration of docker compose, you may need to run `docker-compose` to avoid the command not found error.

### Running the Containers

```sh
docker compose -f filename.yml up -d
```

- `-f filename.yml` – Specifies the compose file to use especially when we have numerous of them that are not given the conventional name of `docker-compose.yml`
- `up -d` – Starts the containers in detached mode.

### Stopping and Removing Containers

```sh
docker compose -f filename.yml down
```

- Stops and removes the containers, network, and volumes.

### Rebuilding Containers

```sh
docker compose -f filename.yml up --build -d
```

- `--build` – Forces a rebuild of images before starting the containers.
- Replace `filename.yml` with relevant name.

### Checking Logs

```sh
docker logs container_name
```

- Shows logs for the specified container for instance `docker logs python-api_postgres-1` shows logs for the container `python-api_postgres-1`.

### Viewing Running Containers

```sh
docker ps
```

- Lists all active containers.
- Use an additional `-a` flag to view all containers including stopped ones.

### Executing Commands Inside the Container

```sh
docker exec -it container_name bash
```

- Opens an interactive shell inside the specified container.

### Explanation of Docker Compose Flags

- `-f` – Specifies a custom compose file (`docker-compose-dev.yml` instead of the default `docker-compose.yml`).
- `-d` – Runs containers in detached mode.
- `--build` – Rebuilds the images before starting the containers.
- `--no-cache` – Prevents Docker from using cached layers during the build process.
- `--remove-orphans` – Removes containers that are not defined in the current compose file.

## Syncing Local Code with Containers (Bind Mounts)

- Issue: Changes in code don’t reflect inside the container.
- Solution: Use a bind mount to sync local files with the container:

  ```yaml
  services:
    fastapi:
      volumes:
        - ./app:/app:ro
  ```

- `./app:/app:ro` syncs local `app` folder with container’s `app` folder.
- `ro` (read-only) ensures container cannot modify source code.

### Debugging Changes Not Reflecting

- If changes aren’t reflected:
  1. Check inside the container:

     ```sh
     docker exec -it fastapi_1 bash
     cat /app/main.py
     ```

  2. If the file updates but changes don’t reflect, ensure auto-reload is enabled in FastAPI:

     ```yaml
     command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
     ```

- `--reload` flag ensures changes are picked up automatically during development.

### Final Steps

- Always stop and restart containers to apply changes:

  ```sh
  docker compose down
  docker compose up -d
  ```

- Verify changes by sending requests and observing responses.

[[TOC]]
