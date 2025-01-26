# SQLAlchemy and ORMs in Python

## Interacting with Databases

- In Python (or other programming languages), there are two primary ways to interact with databases:
  1. Using raw SQL commands via a database driver.
  2. Using an Object Relational Mapper (ORM), such as SQLAlchemy, which provides an abstraction layer.

## Benefits of ORMs

- ORMs like SQLAlchemy allow developers to work with Python code instead of raw SQL commands.
- Tables and columns are defined as Python models.
- Queries can be built using Python methods and objects, abstracting away SQL complexity.
- SQLAlchemy is independent of web frameworks like FastAPI and can be used with any Python application.

## Setting Up SQLAlchemy

### Installation

1. Install SQLAlchemy:

   ```bash
   pip install sqlalchemy
   ```

2. Ensure a database driver is installed (e.g., `psycopg3` for PostgreSQL):

   ```bash
   pip install psycopg
   ```

   > - SQLAlchemy requires a driver to communicate with the database.
   > - For PostgreSQL, we use `psycopg`.

### Database Connection

Create a `database.py` file to manage the database connection.

#### Code Example

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# actual connection details
SQLALCHEMY_DATABASE_URL = "postgresql://postgres+psycopg:password123@localhost/fastapi"

# Create an engine to manage the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure sessionmaker for database interactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Define the base class for ORM models
Base = declarative_base()

# add dependency for database handling
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

#### Explanation

1. **`create_engine()`**
   - Establishes the connection to the database using the provided URL, filling it in with the relevant information:

    ```python
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://<username>:<password>@<hostname>/<database_name>"
    ```

    - Note the use `postgresql+psycopg` which ensures SQLAlchemy uses psycopg3 instead of psycopg2
    - Otherwise, if using the latter, there is no need to include the `+psycopg` part to the string URL

2. **`sessionmaker()`**
   - Creates a session factory for interacting with the database.
   - `autocommit=False`: Transactions are not committed automatically.
   - `autoflush=False`: Prevents automatic flushing of changes to the database.
   - `bind=engine`: Binds the session to the database engine.

3. **`declarative_base()`**
   - Provides a base class for defining ORM models.
   - All models will inherit from this base class.

4. **`get_db()`**
    - The `get_db` function centralizes database session management by opening a session when needed and closing once done
    - That means that there is also no need to hard code connection and using context managers psycopg as before, since it handles them
    - Keeping it in `database.py` aligns it with other database-related configurations, ensuring that `main.py` remains focused on application logic and routing.

!!! Best Practices

- Avoid hardcoding sensitive information like database credentials in the code.
- Use environment variables or a secrets manager instead.

## Defining Models and Tables

To define our tables, we use SQLAlchemy as an ORM, eliminating the need to create tables manually in tools like pgAdmin.

1. **Create a `models.py` file:**
   - Each model in this file corresponds to a table in the database.
   - Import `Base` from your `database.py` file to extend it for your models.

    ```python
    # models.py
    from sqlalchemy import Column, String, Boolean, Integer
    from sqlalchemy.sql import text
    from sqlalchemy.sql.sqltypes import TIMESTAMP

    from .database import Base

    class Post(Base):
        __tablename__ = "posts"

        id = Column(Integer, primary_key=True, nullable=False, index=True)
        title = Column(String, nullable=False)
        content = Column(String, nullable=False)
        published = Column(Boolean, server_default='TRUE', nullable=False)
        created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    ```

    - **`__tablename__`** specifies the name of the table in Postgres.
    - Each attribute of the class represents a column, using `Column` to define types and constraints.
    - Using `server_default` ensures that the default value is set at the database level, not just within the ORM. This is particularly useful when multiple applications or tools interact with the same database, ensuring consistency across all operations.

2. **Integrate Models into the Application:**
   - Import the models in the `main.py` file and ensure that the database tables are created when the application starts.

    ```python
    # main.py
    from fastapi import FastAPI, Depends
    from sqlalchemy.orm import Session
    from . import models
    from .database import engine, get_db

    models.Base.metadata.create_all(bind=engine)

    app = FastAPI()

    @app.get("/sqlalchemy")
    def test_posts(db: Session = Depends(get_db)):
        return {"status": "success"}
    ```

    - **`models.Base.metadata.create_all(bind=engine)`**: This command ensures that all models defined with SQLAlchemy are used to create corresponding tables in the database if they don’t already exist.
    - **`def test_posts(db: Session = Depends(get_db)):`**: The `Depends(get_db)` dependency injects a database session into the endpoint (`/sqlalchemy`), allowing us to interact with the database within the scope of this function. The session is automatically closed after the request is completed.

3. **Verify Table Creation:**
   - When you save and restart the application, SQLAlchemy checks for the table (`posts` in this case). If it doesn’t exist, it will create one based on the model definition.
   - **Note**: If the post table already exists, changes to the model will not be reflected in the database. This is a limitation of SQLAlchemy’s `create_all` method. To address this, use a migration tool like Alembic to manage schema changes effectively or manually delete the table and allow for its recreation

4. **Organizing Code:**
   - Move the `get_db` function and related database initialization code to `database.py` to keep `main.py` uncluttered. Import these components as needed.

This setup streamlines database interactions and prepares your application for scalable and maintainable development.

!!! Explanation

1. **`session.query()`**
   - Initiates a query on the specified model (`User`).

2. **`filter()`**
   - Adds a condition to the query (e.g., `User.name == "John"`).

3. **`.first()`**
   - Fetches the first result from the query.

4. **Session Management**
   - Always close sessions after use to release database connections.

## Difference Between Pydantic Models and SQLAlchemy Models

### Schema (Pydantic) Models

- **Purpose**: Defines the structure of a request and response in APIs.
- **Validation**:
  - Ensures that all fields required in a request are present.
  - Validates data types (e.g., `title` must not be an integer, `published` must be a boolean).
- **Request Handling**:
  - Dictates the shape of data sent from clients (e.g., browsers or mobile devices).
  - Example: Defines required fields for creating or updating a post.
- **Response Handling**:
  - (Optional but recommended) Specifies which fields to include in responses.
  - Allows control over sensitive or unnecessary data sent back to clients.
- **Implementation**:
  - Extends `BaseModel` from the Pydantic library.
  - Used in FastAPI path operations.

!!! Code Example

```python
# Pydantic Schema Model
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: bool
```

### SQLAlchemy Models

- **Purpose**: Defines the structure of database tables.
- **Functionality**:
  - Specifies table columns and attributes.
  - Used to perform queries, create, update, and delete entries in the database.
- **Implementation**:
  - Used for database interactions via SQLAlchemy ORM.

!!! Code Example

```python
# SQLAlchemy Model
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    published = Column(Boolean, default=True)
```

### Comparison: Pydantic vs SQLAlchemy

| Feature                | Pydantic Model                     | SQLAlchemy Model                  |
|------------------------|-------------------------------------|------------------------------------|
| **Purpose**            | Define API request/response schema | Define database table structure    |
| **Validation**         | Ensures correct data in requests   | Not responsible for validation     |
| **Scope**              | API-level                          | Database-level                     |
| **Library**            | `pydantic.BaseModel`               | `sqlalchemy` ORM                   |
| **Focus**              | Shape and validation of data       | Data persistence                   |

---

### Improvements Suggested

- **Separation of Concerns**:
  - Move Pydantic models to a separate file (e.g., `schemas.py`) for better organization.
- **Inheritance for Reusability**:
  - Use a base schema (e.g., `PostBase`) and extend it for specific purposes like `PostCreate` or `PostUpdate`.

!!! Refactoring Example

```python
# schemas.py
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: bool

# main.py
from . import schemas

@app.post("/posts")
def create_post(post: schemas.PostCreate):
    # Logic here
    pass

@app.put("/posts/{id}")
def update_post(post: schemas.PostUpdate):
    # Logic here
    pass
```

### Benefits of Using Pydantic Models

- Strict data validation for requests and responses.
- Prevention of malformed or unexpected data from clients.
- Flexibility to define different schemas for different operations (e.g., create, update, response).

### Benefits of Using SQLAlchemy Models

- Robust ORM for interacting with databases.
- Easy to map Python classes to database tables.
- Simplifies database queries and data manipulation.

[[TOC]]
