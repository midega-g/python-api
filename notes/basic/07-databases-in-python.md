# Working with Database in Python

## Setup in pgAdmin

### 1. Delete the Products Table

- Navigate to the `products` table in your database.
- Right-click on the table and select `Delete` or `Drop`.
- Confirm the deletion if prompted.
- **Note**: If you want to keep the table for reference, you can skip this step as it won't affect the rest of the process.

### 2. Switch to the FastAPI Database

- Move to the FastAPI database if you're working on a different machine or database instance.
- Ensure you focus only on the FastAPI database, ignoring other databases that might appear.

### 3. Define the Table Structure for Posts

- Analyze the application requirements to determine the columns for the `posts` table:
  - `id`: A unique identifier for each post.
  - `title`: The title of the post.
  - `content`: The main content of the post.
  - `published`: A boolean indicating whether the post is published (default: `true`).
  - `created_at`: A timestamp to track when the post was created.

### 4. Create the Posts Table

- Use the following SQL query to create the `posts` table:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### Explanation

- `id SERIAL PRIMARY KEY`: Auto-incrementing primary key for unique identification.
- `title VARCHAR NOT NULL`: Title of the post, cannot be NULL.
- `content VARCHAR NOT NULL`: Content of the post, cannot be NULL.
- `published BOOLEAN NOT NULL DEFAULT TRUE`: Boolean flag indicating if the post is published, defaults to TRUE.
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`: Timestamp with timezone, automatically set to the current time.

### 5. Insert Sample Data into the Posts Table

- Manually add sample posts using your database tool's data editor or SQL queries.
- Example posts:
  - First post: Title: "This is my first post", Content: "Interesting stuff"
  - Second post: Title: "This is my second post", Content: "More interesting stuff"

### 6. Verify the Data in the Table

- Use the following SQL query to verify the data in the `posts` table:

```sql
SELECT * FROM posts;
```

- Ensure the data matches the inserted values.

### 7. Save Changes

- Save the table and data modifications.
- You are now ready to proceed with further operations on the `posts` table.

## Setup in Python

### Step 1: Install the Database Driver

To work with a PostgreSQL database in Python, install the `psycopg3` library, as we will use it for database interactions:

```python
pip install psycopg
```

### Step 2: Database Connection

Here’s how to connect to a PostgreSQL database using `psycopg3` with retry logic and a separate function for managing the connection:

```python
import psycopg
from psycopg.rows import dict_row
import time

# Maximum retries for database connection
MAX_RETRIES = 5

def connect_to_db():
    """Attempts to connect to PostgreSQL with retries."""
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            connection = psycopg.connect(
                user="postgres",
                password="password",
                host="localhost",
                port="5432",
                dbname="fastapi",
                row_factory=dict_row,
            )
            print("✅ Connection to PostgreSQL DB successful")
            return connection
        except psycopg.Error as e:
            print(f"⚠️ Error: {e}")
            retry_count += 1
            print(f"Retrying in 5 seconds... {retry_count}/{MAX_RETRIES}")
            time.sleep(5)

    print("❌ Max retries reached. Could not connect to the database.")
    return None  # Return None if connection fails
```

!!! Explanation of Code

- **Retry Logic**: Attempts to connect to the database up to `MAX_RETRIES` times, with a 5-second delay between retries.
- **Context Managers (`with`)**: Although not used here, will be demonstrated in subsequent sections for resource management.
- **`row_factory=dict_row`**: Ensures SQL query results are returned as dictionaries.

!!! Keep in Mind

- Hardcoding database credentials in the source code is a security risk.
- For now, we are using hardcoded values for simplicity.
- In a production environment, use environment variables to dynamically configure database connections.

### Step 3: Creating a Table

The following function creates the `posts_3` table if it does not already exist:

```python
def create_table(connection):
    """Creates the posts_3 table if it does not exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS posts_3 (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        content TEXT NOT NULL,
        published BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("✅ Table 'posts_3' created successfully")
    except psycopg.Error as e:
        print(f"⚠️ Error creating table: {e}")
```

!!! Explanation of SQL Query

- **`CREATE TABLE IF NOT EXISTS`**: Ensures the table is only created if it does not already exist.
- **`id SERIAL PRIMARY KEY`**: Auto-incrementing integer to uniquely identify rows.
- **`published BOOLEAN DEFAULT TRUE`**: Column defaults to `TRUE` if no value is specified.
- **`created_at TIMESTAMPTZ DEFAULT NOW()`**: Timestamp of row creation.

### Step 4: Inserting Data

The following function inserts new rows into the `posts_3` table:

```python
def insert_post(connection, title, content, published=True):
    """Inserts a new post into the posts_3 table."""
    insert_query = """
    INSERT INTO posts_3 (title, content, published)
    VALUES (%s, %s, %s);
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, (title, content, published))
            connection.commit()
            print(f"✅ Post '{title}' inserted successfully")
    except psycopg.Error as e:
        print(f"⚠️ Error inserting post: {e}")
```

!!! Explanation of Insert Query

- **Placeholders (`%s`)**: Prevent SQL injection by parameterizing the query.
- **Default Values**: The `published` column defaults to `TRUE` if not explicitly specified.

### Step 5: Querying Data

The following function retrieves all rows from the `posts_3` table:

```python
def query_posts(connection):
    """Fetches all posts from the posts_3 table."""
    select_query = "SELECT * FROM posts_3;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            print("📜 Retrieved posts:")
            for row in rows:
                print(row)
    except psycopg.Error as e:
        print(f"⚠️ Error querying posts: {e}")
```

!!! Explanation

- **Select Query**: Fetches all rows from the `posts_3` table.
- **Output**: Rows are printed one by one, returned as dictionaries due to `row_factory`.

### Step 6: Running the Code

```python
if __name__ == "__main__":
    db_connection = connect_to_db()

    if db_connection:
        create_table(db_connection)
        insert_post(db_connection, "My First Post", "This is the content of my first post", True)
        insert_post(db_connection, "Second Post", "Another interesting post", False)
        query_posts(db_connection)

        db_connection.close()  # Close connection after operations
        print("🔌 PostgreSQL connection closed")
```

!!! Final Notes

- **Connection Management**: Always close the database connection after operations.
- **Error Handling**: Ensure robust error handling for all database operations.
- **Modular Design**: Functions separate concerns, making the code easier to test and maintain.

[[TOC]]
