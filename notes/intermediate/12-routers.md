# Organizing Path Operations with FastAPI Routers

## Problem: Main.py File Clutter

- **Current State:**
  - All path operations (e.g., for posts and users) are in a single `main.py` file.
  - As the app grows, managing everything in one file becomes unmanageable.

## Solution: Using Routers

- **Routers in FastAPI:**
  - A feature to split path operations into multiple files for better organization.
  - Common across web frameworks.

## Steps to Refactor Code Using Routers

### 1. Create a `routers` Folder

- **Structure:**
  - Create a folder named `routers`.
  - Inside `routers`, create two files:
    - `post.py` (handles all post-related routes).
    - `user.py` (handles all user-related routes).

### 2. Move Path Operations

- **Action:**
  - Move post-related path operations from `main.py` to `post.py`.
  - Move user-related path operations from `main.py` to `user.py`.

### 3. Handle Imports

- **Import Requirements:**
  - Import dependencies into each file (e.g., `models`, `schemas`, `utils`).
  - Use relative imports to access modules outside the `routers` folder.

#### Example: Importing Modules

- **User File Imports:**

  ```python
  from .. import models, schemas, utils
  from fastapi import status, APIRouter
  from sqlalchemy.orm import Session
  from ..database import get_db
  ```

- **Adjustments:**
  - Use `..` to go up one directory when importing from `app`.

### 4. Replace `app` with `router`

- **Router Object:**
  - Import and use `APIRouter`:

    ```python
    from fastapi import APIRouter
    router = APIRouter()
    ```

  - Replace `app` with `router` in all path operations.

### 5. Update Main.py to Include Routers

- **Include Routers:**
  - Import the routers from the `routers` folder:

    ```python
    from .routers import post, user
    ```

  - Use `app.include_router()` to register the routers:

    ```python
    app.include_router(post.router)
    app.include_router(user.router)
    ```

## Testing the Refactored Code

- **Verify Functionality:**
  - Ensure all routes (GET, POST, DELETE, etc.) work as before.
  - Example: Test CRUD operations for posts and users.

## Benefits of Using Routers

- **Cleaner Code:**
  - `main.py` only includes high-level API configuration.
  - Path operations are organized into dedicated files.
- **Scalability:**
  - Add new files to `routers` for additional resources without cluttering `main.py`.

---

### Example Directory Structure

```plaintext
app/
|-- main.py
|-- routers/
    |-- post.py
    |-- user.py
|-- models.py
|-- schemas.py
|-- utils.py
|-- database.py
```

## Simplifying and Grouping Path Operations

### Problem: Repetition of Route Paths

- **Current State:**
  - Routes for posts and users repeatedly use the same base path (e.g., `/posts`, `/users`).
  - This repetition adds unnecessary clutter, especially in larger APIs.

### Solution: Using the `prefix` Parameter

- **FastAPI Feature:**
  - Routers can take a `prefix` parameter to define a base path for all routes in a file.
  - Reduces repetition and improves readability.

### Steps to Implement Prefixes

1. Define a Prefix for Each Router

    - **Add Prefix in `post.py`:**

      ```python
      router = APIRouter(prefix="/posts")
      ```

    - **Add Prefix in `user.py`:**

      ```python
      router = APIRouter(prefix="/users")
      ```

2. Update Route Paths

    - **Simplify Paths:**
      - Remove the repeated base path (`/posts`, `/users`) from individual route definitions.
      - Example:

        ```python
        @router.get("/")
        def get_posts():
            # code here
        ```

        This route will now respond to `/posts`.

3. Test the Updated Routes

    - **Verify Functionality:**
      - Ensure all CRUD operations for posts and users work as expected.
      - Example: Test routes for getting, creating, and deleting posts/users.

### Benefits of Using Prefixes

- **Simpler Code:**
  - Base paths are defined once, reducing redundancy.
- **Easier Maintenance:**
  - Changes to base paths only require updating the `prefix` parameter.

## Improving API Documentation with Tags

### Problem: Lack of Grouping in Documentation

- **Current State:**
  - Swagger UI lists all routes in a single group.
  - Makes it harder to identify related routes (e.g., post-related vs. user-related).

### Solution: Using Tags for Grouping

- **FastAPI Feature:**
  - Tags allow grouping of routes in Swagger UI.
  - Improves readability and usability for clients.

### Steps to Add Tags

1. Assign Tags to Routes

    - **Add Tags in `post.py`:**

      ```python
      router = APIRouter(prefix="/posts", tags=["Posts"])
      ```

    - **Add Tags in `user.py`:**

      ```python
      router = APIRouter(prefix="/users", tags=["Users"])
      ```

2. Verify Documentation

    - **Check Swagger UI:**
    - Navigate to `/docs`.
    - Ensure routes are grouped under the appropriate tags (e.g., Posts, Users).

### Benefits of Using Tags

- **Enhanced Readability:**
  - Related routes are grouped together in the documentation.
- **Better Usability:**
  - Clients can quickly identify and test relevant routes.

[[TOC]]
