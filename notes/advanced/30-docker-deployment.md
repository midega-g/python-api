# Docker Hub and Repository Setup

## Creating a Docker Hub Account and Repository

1. Go to [Docker Hub](https://hub.docker.com/) and create a free account.
2. Navigate to `Repositories` and select `Create Repository`.
3. Give your repository a name (e.g., `python-api-v1`).
4. Choose `Public` (you only get one private repository for free).
5. Your repository URL will be structured as: `your-username/your-repo-name`.

## Uploading an Image to Docker Hub

### Check Existing Docker Images

Run:

```bash
docker image ls
```

Find the image you want to upload.

### Log in to Docker Hub

```bash
docker login
```

Enter your Docker Hub credentials.

### Tagging the Image

Docker images must be tagged in the format `username/repository[:tag]`, where `tag` if the version but it is optional.

```bash
docker image tag <image-id> your-username/your-repo-name
```

Example:

```bash
docker image tag fastapi_api sloppy-networks/fastapi
```

Check the new tag:

```bash
docker image ls
```

### Pushing the Image

```bash
docker push your-username/your-repo-name
```

Example:

```bash
docker push midega/python-api-v1
```

Once pushed, verify on Docker Hub by refreshing the repository page.

## Docker Environments: Development & Production

### Why Separate Dev and Prod?

- Development and production environments should be similar but have differences:
  - No `--reload` flag in production.
  - No bind mounts in production.
  - Different port configurations.
  - Use environment variables instead of hardcoded values.

## Creating Separate Docker Compose Files

1. Stop running containers:

   ```bash
   docker compose down
   ```

2. Copy the existing `docker-compose.yaml` file and rename:

   ```bash
   cp docker-compose.yaml docker-compose-dev.yml
   cp docker-compose.yaml docker-compose-prod.yml
   ```

3. Modify `docker-compose-prod.yaml`:
   - Remove `--reload` from `command`.
   - Change the port mapping (e.g., `8000:80`).
   - Use environment variables:

     ```yaml
     environment:
       - DATABASE_HOSTNAME=${DATABASE_HOSTNAME}
       - DATABASE_PORT=${DATABASE_PORT}
       - DATABASE_NAME=${DATABASE_NAME}
       - DATABASE_USERNAME=${DATABASE_USERNAME}
       - DATABASE_PASSWORD=${DATABASE_PASSWORD}
     ```

   - Remove bind mounts.
   - Use an image from Docker Hub instead of building:

     ```yaml
     services:
       app:
         image: your-username/your-repo-name
     ```

- The final Docker Compose file for production is available [here](../../docker-compose-prod.yml)

## Running the Correct Docker Compose File

- For development:

  ```bash
  docker compose -f docker-compose-dev.yml up -d
  ```

- For production:

  ```bash
  docker compose -f docker-compose-prod.yml up -d
  ```

- To check if things are working correctly, go to Postman and configure a url variable with the values `http://0.0.0.0:8080` or the one that you've predefined during the port mapping of `api` service

- Stopping a specific environment:

  ```bash
  docker compose -f docker-compose-prod.yml down
  ```

## Best Practice: Pull Image in Production

Instead of building the image in production, pull from Docker Hub:

1. Push the new image to Docker Hub after development.
2. Modify `docker-compose-prod.yaml` to use the latest image.
3. Deploy using:

   ```bash
   docker compose -f docker-compose-prod.yml up -d
   ```

This ensures a stable, production-ready environment.
