# Deployment to Render

Deploying a FastAPI application with Alembic migrations to **Render** involves several steps. Here, we will cover a detailed guide to help with the deployment of application successfully.

## Prerequisites

1. **Render Account**: Sign up at [Render](https://render.com/).
2. **GitHub Repository**: Ensure your project is hosted on GitHub.
3. **Environment Variables**: Prepare all required environment variables (e.g., database credentials, secrets).

## Step 1: Prepare Application for Deployment

**NOTE:**

- If you've followed along instructions from [these notes](../intermediate/25-alembic-database-migration-tool.md), then the first two steps are optional.
- Other optional steps are 4 and 5 depending on the package management tool that you've used.

### 1. **(Optional) Update `alembic.ini`**

- Modify the `sqlalchemy.url` in `alembic.ini` to use environment variables for the database connection:

     ```ini
     sqlalchemy.url = ${DATABASE_URL}
     ```

- This ensures Alembic uses the correct database URL during deployment.

### 2. **(Optional) Update `env.py`**

- Ensure `env.py` in the `alembic` directory dynamically reads the database URL from environment variables:

     ```python
     import os
     from alembic import context

     config = context.config
     config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
     ```

### 3. **Create a `start.sh` Script**

- Create a shell script to run your application and apply Alembic migrations:

     ```bash
     #!/bin/bash

     # Ensure Alembic migrations are applied automatically during deployment
     alembic upgrade head

     # Use Render's provided PORT if available, otherwise default to 8000
     PORT=${PORT:-8000}

     # Start the FastAPI application with the selected port
     uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
     ```

- Make the script executable (use sudo mode if required):

     ```bash
     chmod +x start.sh
     ```

### 4. **(Optional) Update `pyproject.toml`**

- Ensure your `pyproject.toml` includes all dependencies required for deployment:

     ```toml
     [tool.poetry.dependencies]
     fastapi = "^0.95.0"
     uvicorn = "^0.21.0"
     alembic = "^1.10.2"
     psycopg2 = "^2.9.5"
     ```

### 5. **(Optional) Add a `.env` File**

- If you use `python-dotenv` to load environment variables locally, create a `.env` file:

     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/dbname
     ```

- **Note**: Do not commit this file to GitHub. Add it to `.gitignore`:

     ```gitignore
     .env
     ```

## Step 2: Set Up a PostgreSQL Database on Render

1. **Create a PostgreSQL Database**:
   - Go to the Render dashboard and click **New > PostgreSQL**.
   - Configure the database (name, region, etc.).
   - Note the **External Database URL** provided by Render.

2. **Add Environment Variables**:
   - Add the following environment variables to your Render project:
     - `DATABASE_URL`: The external database URL from Render.
     - Other required variables (e.g., `SECRET_KEY`, `ALGORITHM`).

## Step 3: Deploy to Render

### 1. **Create a New Web Service**

- Go to the Render dashboard and click **New > Web Service**.
- Connect your GitHub repository.

### 2. **Configure the Web Service**

- **Name**: Choose a name for your service.
- **Region**: Select a region close to your users.
- **Branch**: Select the branch to deploy (e.g., `main`).
- **Build Command**:

     ```bash
     poetry install --no-dev
     ```

- **Start Command**:

     ```bash
     ./start.sh
     ```

### 3. **Add Environment Variables**

- Add the environment variables required for your application (e.g., `DATABASE_URL`, `SECRET_KEY`).

### 4. **Deploy**

- Click **Create Web Service** to start the deployment process.

## Step 4: Verify Deployment

1. **Check Logs**:
   - Monitor the deployment logs in the Render dashboard to ensure there are no errors.
   - Look for messages indicating that Alembic migrations were applied successfully.

2. **Test the API**:
   - Once deployed, test your API using the provided Render URL (e.g., `https://your-service.onrender.com`).
   - Use tools like Postman or `curl` to verify endpoints.

## Folder Structure After Deployment

Your final folder structure should look like this:

```
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── 618fe20d1b88_create_inital_schema.py
├── alembic.ini
├── app
│   ├── config.py
│   ├── database.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── routers
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── user.py
│   │   └── vote.py
│   ├── schemas.py
│   └── utils.py
├── env_
├── poetry.lock
├── pyproject.toml
├── README.md
├── start.sh
└── test-codes
    ├── fastapi-test-queries.sql
    ├── psycopg-test.py
    └── test.py
```

## Troubleshooting

### 1. **Database Connection Issues**

- Verify that the `DATABASE_URL` environment variable is correctly set in Render.
- Ensure the PostgreSQL database is running and accessible.

### 2. **Alembic Migration Errors**

- Check the logs for errors during the `alembic upgrade head` command.
- Ensure the `alembic.ini` and `env.py` files are correctly configured.

### 3. **Application Fails to Start**

- Verify that all dependencies are installed (`poetry install --no-dev`).
- Check the `start.sh` script for errors.
