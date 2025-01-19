import time

import psycopg
from psycopg.rows import dict_row

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


if __name__ == "__main__":
    db_connection = connect_to_db()

    if db_connection:
        create_table(db_connection)
        insert_post(
            db_connection,
            "My First Post",
            "This is the content of my first post",
            True,
        )
        insert_post(
            db_connection, "Second Post", "Another interesting post", False
        )
        query_posts(db_connection)

        db_connection.close()  # Close connection after operations
        print("🔌 PostgreSQL connection closed")
