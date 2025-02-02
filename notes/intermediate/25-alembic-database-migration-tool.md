# SQL Alchemy and Alembic

## SQLAlchemy Limitations

- **Modification Restrictions**: SQLAlchemy does not allow modifications to existing tables (e.g., adding/deleting columns, adding foreign keys).
- **Table Creation**: SQL Alchemy only creates tables if they do not already exist in the database.
- **Workaround**: To apply changes, tables must be dropped and recreated, which is not feasible in production.

## Alembic: Database Migration Tool

- **Purpose**: Alembic allows for incremental changes to the database schema and tracks these changes over time.
- **Benefits**:
  - Automatically updates the database schema based on model definitions.
  - Tracks changes and allows rollbacks to previous states.
  - Similar to version control for databases (like Git for code).

## Removing SQL Alchemy's `create_all`

- With Alembic, the `create_all` command in SQL Alchemy defined in `main.py` is no longer necessary. Thus, comment it out or remove it from the the application:

  ```python
  Base.metadata.create_all(bind=engine)
  ```

## Setting Up Alembic

1. **Install Alembic**:

   ```bash
   pip install alembic
   ```

2. **Initialize Alembic**:

   ```bash
   alembic init alembic
   ```

    - The command initializes Alembic in our FastAPI project, setting up the necessary files and directory structure for database migrations.
    - It does the following:

    1. **Creates an `alembic/` Directory**
        - This directory will contain migration scripts and configuration files.
        - It is the workspace where Alembic tracks changes to the database schema.

    2. **Generates an `alembic.ini` File**
        - This is the main configuration file for Alembic.
        - It contains database connection settings and configuration options.

3. **Configure `env.py`**:
   - In the `alembic` directory, locate the `env.py` file and import the `Base` object from your SQL Alchemy models:

     ```python
     from app.models import Base
     ```

      - The `Base` object is the declarative base class for your SQL Alchemy models. By importing it, Alembic gains access to all the table and column definitions in your application.
      - This allows Alembic to generate migrations based on changes in your SQL Alchemy models.

   - Set `target_metadata` to `Base.metadata` instead of `None`:

     ```python
     target_metadata = Base.metadata
     ```

      - `target_metadata` is a required configuration in Alembic. It tells Alembic which metadata object to use for tracking database schema changes.
      - By setting `target_metadata = Base.metadata`, Alembic will use the metadata from your SQL Alchemy models to detect changes and generate migrations.

4. **Configure `alembic.ini` (Hardcoding Credentials)**:
   - Set the `sqlalchemy.url` to your database connection string:

     ```ini
     sqlalchemy.url = postgresql://username:password@localhost:5432/database_name
     ```

   - However, hardcoding the database URL directly in `alembic.ini` is **not secure** because it exposes sensitive information like our database username and password.
   - This is especially risky if the file is committed to version control (e.g., Git) and shared publicly.

5. **Second Option (Using Environment Variables)**:

   - Alternatively, override the URL in `env.py` using environment variables:

     ```python
     from app.config import settings

     config.set_main_option(
      "sqlalchemy.url",
      f"postgresql+psycopg://{settings.DATABASE_USERNAME}:"
      f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:"
      f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
     )
     ```

   - Overriding the URL in `env.py` using environment variables is the **recommended approach**.
   - This keeps sensitive information out of your codebase and allows you to manage credentials securely (e.g., using `.env` files or a secrets manager).

## Importance of the Alembic Directory and Files

### `alembic.ini` (Configuration File)

- Defines the database connection URL.
- Contains settings for logging, script generation, and migration environment.
- The `sqlalchemy.url` key needs to be updated with the correct database URL.

### `alembic/` Directory (Migration Workspace)

- **Versions (`alembic/versions/`)**
  - Stores migration scripts that track schema changes over time.
  - Each migration file is timestamped and contains upgrade/downgrade instructions.
- **`env.py`**
  - Configures the migration environment.
  - Imports the database models and sets up the database connection.
- **`script.py.mako`**
  - Template for generating new migration scripts.

## Alembic Commands and Usage

### Auto-Generate Migrations

**Purpose:**

- Automatically detect changes in SQL Alchemy models and generate the necessary migration scripts.
- This is useful for creating tables, adding columns, or modifying the database schema based on changes in your models.

**Commands:**

1. **Generate a Migration Script**:

   ```bash
   alembic revision --autogenerate -m "create all tables defined"
   ```

   - This command:
     - Compares the current state of our SQL Alchemy models with the current state of the database.
     - Generates a migration script in the `versions` directory with the necessary changes (e.g., creating tables, adding columns).
     - The `-m` flag allows us to add a descriptive message for the migration.
   - It should be used When we’ve made changes to our models (e.g., added a new table or column) and want to automatically generate a migration script.

2. **Apply the Migration**:

   ```bash
   alembic upgrade head
   ```

   - This command:
     - Applies all pending migrations up to the latest revision (`head`).
     - Updates the database schema to match the current state of your models.
   - **Alternative**:
     - We can also specify a specific revision ID to upgrade to:

       ```bash
       alembic upgrade <revision_id>
       ```

       - This applies all migrations up to and including the specified revision.

### Example Workflow

1. **Add a Column**:
   - Add a `published` column to the `posts` table in your model:

     ```python
     published = Column(Boolean, server_default='TRUE', nullable=False)
     ```

   - Generate the migration script:

     ```bash
     alembic revision --autogenerate -m "added published column to the posts table"
     ```

   - Apply the migration:

     ```bash
     alembic upgrade head
     ```

## More Commands Explained

### 1. **Create a Migration Revision (Manually)**

```bash
alembic revision -m "description_of_changes"
```

- **Creates a new migration script** in the `versions/` directory.
- The script contains `upgrade()` and `downgrade()` functions where changes must be defined.
- Use when making **manual** schema changes.

### 2. **Rollback Migrations (Downgrade Database)**

```bash
alembic downgrade <revision_id>
```

- Rolls back schema changes to a specified revision.
- To undo the last migration:

```bash
alembic downgrade -1
```

### 3. **Check Current Migration State**

```bash
alembic current
```

- Displays the current applied migration.

### 4. **View Migration History**

```bash
alembic history
```

- Lists all migration revisions and their applied status.

## Example Workflows

### 1. **Creating a Table**

- **Create a Revision:**

```bash
alembic revision -m "create_post_table"
```

- **Define `upgrade()` and `downgrade()`** in the relevant version file in the generated by the command above:

```python
def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False)
    )

def downgrade():
    op.drop_table('posts')
```

- **Apply the Migration:**

```bash
alembic upgrade head
```

### 2. **Adding a Column**

- **Create a Revision:**

```bash
alembic revision -m "add_content_column_to_posts"
```

- **Define `upgrade()` and `downgrade()`**

```python
def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))

def downgrade():
    op.drop_column('posts', 'content')
```

- **Apply the Migration:**

```bash
alembic upgrade head
```

### 3. **Adding a Foreign Key**

- **Create a Revision:**

```bash
alembic revision -m "add_foreign_key_to_posts"
```

- **Define `upgrade()` and `downgrade()`:**

```python
def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'posts_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
```

- **Apply the Migration:**

```bash
alembic upgrade head
```

## Summary of Key Alembic Commands

| Command | Description |
|---------|-------------|
| `alembic init alembic` | Initializes Alembic in your project |
| `alembic revision -m "message"` | Creates a new migration script |
| `alembic revision --autogenerate -m "message"` | Auto-generates migration script from model changes |
| `alembic upgrade head` | Applies all pending migrations |
| `alembic downgrade -1` | Rolls back the last migration |
| `alembic current` | Shows the current applied migration |
| `alembic history` | Displays migration history |

## Best Practices

- **Avoid Hardcoding**: Use environment variables for sensitive data like database credentials.
- **Regular Migrations**: Create migrations frequently to keep the database schema in sync with the application models.
- **Test Migrations**: Always test migrations in a development environment before applying them to production.

[[TOC]]
