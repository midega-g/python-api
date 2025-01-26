# Handling PostgreSQL Database Connection in Python

## Overview

This guide explains how to use the psycopg3 library with a context manager to handle PostgreSQL database connections in Python. We'll also demonstrate how to retrieve and create posts in a "posts" table, using best practices like parameterized queries to avoid SQL injection.

## Retrieving All Posts

!!! Code Example

```python
@app.get("/posts")
def get_posts():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts;")
        posts = cursor.fetchall()
    return {"data": posts}
```

!!! Explanation

1. **`with connection.cursor()`**: Creates a context manager for the cursor, ensuring it is automatically closed after the block.
2. **`cursor.execute("SELECT * FROM posts;")`**: Executes the SQL query to retrieve all rows from the "posts" table.
3. **`cursor.fetchall()`**: Retrieves all rows from the executed query result.
4. **`return {"data": posts}`**: Returns the data as a JSON response.

## Creating a New Post

!!! Code Example

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post = Body(...)):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO posts (title, content, published)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (post.title, post.content, post.published)
        )
        new_post = cursor.fetchone()  # Fetch the inserted row
        connection.commit()  # Save the changes to the database
    return {"data": new_post}
```

!!! Explanation

1. **`with connection.cursor()`**: Ensures the cursor is properly managed and closed after use.
2. **`cursor.execute()`**:
   - Executes an `INSERT` statement to add a new post to the "posts" table.
   - The `RETURNING *` clause fetches the newly inserted row.
3. **Parameterized Queries**:
   - `%s` placeholders prevent SQL injection by sanitizing user inputs.
   - The tuple `(post.title, post.content, post.published)` maps to these placeholders.
4. **`cursor.fetchone()`**:
   - Retrieves the first row from the query result, which in this case is the newly inserted row.
5. **`connection.commit()`**:
   - Commits the staged changes to the database, ensuring they are saved permanently.
6. **`return {"data": new_post}`**:
   - Sends the newly created post back as a JSON response.

## Why Use Parameterized Queries?

Using string interpolation to build SQL statements can leave your application vulnerable to SQL injection attacks. By using `%s` placeholders and passing parameters separately, psycopg3 ensures:

- Inputs are properly escaped.
- Malicious SQL commands in user inputs are neutralized.

!!! note Example of Vulnerable Code

```python
# DO NOT USE THIS METHOD
cursor.execute(f"INSERT INTO posts (title, content) VALUES ('{title}', '{content}')")
```

If `title` contains a malicious SQL command, it could compromise your database.

!!! Secure Code with Parameterized Queries

```python
cursor.execute(
    "INSERT INTO posts (title, content) VALUES (%s, %s)",
    (title, content)
)
```

## Fetching, Updating, and Deleting a Single Post

### Helper Function: Finding a Post or Raising a 404 Error

- A helper function, `find_post_or_404()`, is defined to centralize and standardize the logic for fetching posts across CRUD operations. This ensures consistent error handling and reduces code duplication.
- The function retrieves a post by its ID and raises an HTTP 404 error if the post is not found.

  ```python
  # Helper function to find a post by ID or raise a 404 exception.
  def find_post_or_404(post_id):
      with connection.cursor() as cursor:
          cursor.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
          post = cursor.fetchone()
      if not post:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Post with id: {post_id} was not found",
          )
      return post
  ```

- **Purpose and Benefits:**
  - Centralizes error handling for missing posts, avoiding repetitive code.
  - Ensures uniform error messages for API consumers.
  - Reduces unnecessary database queries by pre-checking post existence.

### Fetching a Post

- The `get_post` function retrieves a post by its ID using the helper function `find_post_or_404` and returns the data in a structured format.

  ```python
  # Fetch a post by its ID.
  @app.get("/posts/{post_id}")
  def get_post(post_id: int):
      post = find_post_or_404(post_id)
      return {"data": post}
  ```

- **Key Points:**
  - Ensures a valid post exists before attempting to fetch it.
  - Returns structured data, making it easier for API consumers to process the response.

### Deleting a Post

- The `delete_post` function handles post deletion in a secure and efficient manner.

  ```python
  # Delete a post by its ID.
  @app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
  def delete_post(post_id: int):
      find_post_or_404(post_id)
      with connection.cursor() as cursor:
          cursor.execute(
              "delete from posts where id = %s returning *;", (post_id,)
          )
          connection.commit()
      return Response(status_code=status.HTTP_204_NO_CONTENT)
  ```

- **Steps:**
  1. Ensures the post exists by calling `find_post_or_404`.
  2. Deletes the post using a parameterized SQL query to prevent SQL injection.
  3. Commits the transaction to save changes.
  4. Returns a `204 No Content` response, indicating successful deletion without additional data.

- **Why This Approach is Necessary:**
  - Pre-checking the post’s existence avoids attempting to delete a non-existent resource.
  - Parameterized queries ensure security by mitigating SQL injection risks.
  - Returning a `204` status provides a clear and concise confirmation of success.

### Updating a Post

- The `update_post` function modifies an existing post with new data provided by the user.

  ```python
  # Update an existing post with new data.
  @app.put("/posts/{post_id}")
  def update_post(post_id: int, post: Post = Body(...)):
      find_post_or_404(post_id)
      post_dict = post.model_dump()
      with connection.cursor() as cursor:
          cursor.execute(
              """
              update posts
              set title = %s, content = %s, published = %s
              where id = %s
              returning *
              """,
              (
                  post_dict["title"],
                  post_dict["content"],
                  post_dict["published"],
                  post_id,
              ),
          )
          updated_post = cursor.fetchone()
          connection.commit()
      return {"data": updated_post}
  ```

- **Steps:**
  1. Validates the post’s existence using `find_post_or_404`.
  2. Converts the `Post` object into a dictionary using `model_dump()` to ensure the data is clean and validated.
  3. Updates the post’s details using a parameterized SQL query.
  4. Commits the changes to persist the updates.
  5. Returns the updated post data for confirmation.

- **Key Considerations:**
  - Using `find_post_or_404` prevents errors related to modifying non-existent posts.
  - `model_dump()` ensures input data is sanitized and validated before use, enhancing security and consistency.
    - It validates the input against the `Post` schema and converts it into a format suitable for database operations, minimizing the risk of malformed or insecure data.
  - Returning the updated post data provides immediate feedback to the API consumer.

## Summary Best Practices

- **Context Handling:** The `with` statement ensures proper cleanup of database connections and cursors.
- **Parameterization:** Using `%s` placeholders prevents SQL injection attacks.
- **Transactions:** Explicitly committing changes (`connection.commit()`) ensures data persistence.
- **Error Handling:** Centralized error management via `find_post_or_404` improves code readability and maintainability.
- **Efficiency:** Operations like `fetchone()` avoid unnecessary overhead when only a single record is needed.
- **Data Validation:** Transforming inputs using `model_dump()` ensures data integrity and security as only clean and structured data is processed
- **Meaningful Responses:** Providing clear and concise feedback (e.g., `204 No Content` or updated post data) enhances the user experience and API clarity.

[[TOC]]
