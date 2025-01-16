# CRUD Operations

## What is CRUD?

CRUD is an acronym that stands for the four main functions of an application:

- **Create**: Add new data or entries (e.g., creating a post).
- **Read**: Retrieve or view data (e.g., reading posts or a specific post).
- **Update**: Modify existing data (e.g., updating a post).
- **Delete**: Remove data (e.g., deleting a post).

These functions are fundamental to most applications, such as social media platforms, databases, and more.

## Standard Conventions for CRUD API Design

When designing an API for a CRUD application, it is important to follow standard conventions:

1. Use plural nouns for resource names (e.g., `/posts` instead of `/post`).
2. Utilize HTTP methods corresponding to each operation:
   - `POST` for creating.
   - `GET` for reading.
   - `PUT` or `PATCH` for updating.
   - `DELETE` for deleting.

- Note that `PUT` updates all fields while `PATCH` updates specified fields.

## CRUD Operations in FastAPI

Below are the implementations and explanations for CRUD operations in FastAPI:

- Posts are stored in the `my_posts` array, which is reset every time the server restarts since the data is stored in memory.
- Hardcoded initial posts ensure data availability for testing purposes.

```python
my_posts = [
    {"id": 1, "title": "Post 1", "content": "Content of post 1", "published": True, "rating": 4},
    {"id": 2, "title": "Favorite Foods", "content": "I like pizza", "published": False, "rating": 5},
]
```

### 1. **Create**

- **Functionality**: Adds a new post.
- **HTTP Method**: `POST`
- **Endpoint**: `/posts`

```python
@app.post("/posts")
def create_post(post: Post = Body(...)):
    """
    Adds a new post to the in-memory storage.
    """
    post_dict = post.model_dump()
    post_dict["id"] = len(my_posts) + 1  # Generates a unique ID based on the array length
    my_posts.append(post_dict)
    return {"data": my_posts}
```

**Explanation**:

- A global `my_posts` array is used to store posts in memory.
- Each post gets a unique `id` generated based on the array's length.
- New posts are appended to the array.

### 2. **Read**

#### a. Retrieve All Posts

- **Functionality**: Retrieves all posts.
- **HTTP Method**: `GET`
- **Endpoint**: `/posts`

```python
@app.get("/posts")
def get_posts():
    """
    Retrieves all posts stored in memory.
    """
    return {"data": my_posts}
```

#### b. Retrieve a Specific Post

- **Functionality**: Retrieves a single post by its unique identifier.
- **HTTP Method**: `GET`
- **Endpoint**: `/posts/{id}`
  - The `id` field in the endpoint is known as a **path parameter**.

```python
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Retrieves a specific post by its ID.
    """
    # Uses a generator expression to find the post with the matching ID
    post = next((p for p in my_posts if p["id"] == post_id), None)
    if not post:
        return {"error": f"Post with id {post_id} not found"}
    return {"data": post}
```

**Explanation**:

- `@app.get` specifies the `GET` method.
- The function uses a generator expression (`next((p for p in my_posts if p["id"] == post_id), None)`) to locate the post.
  - This approach iterates through the `my_posts` array until it finds the first match or returns `None` if no match exists.
- Returns an error message if the post is not found.
- Note: Path parameters are received as strings by default. Explicitly defining `post_id: int` ensures proper type handling and prevents unexpected behavior
- Since we'll also use the syntax in `UPDATE` and `DELETE`, a function to handle this would be:

    ```python
    def find_post_or_404(post_id: int):
        """Helper function to find a post by ID or raise a 404 exception."""
        post = next((p for p in my_posts if p["id"] == post_id), None)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found"
            )
        return post
    ```

### 3. **Update**

- **Functionality**: Updates an existing post.
- **HTTP Method**: `PUT` or `PATCH`
- **Endpoint**: `/posts/{id}`

```python
@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: dict):
    """
    Updates the post identified by its ID.
    """
    post = next((p for p in my_posts if p["id"] == post_id), None)
    if not post:
        return {"error": f"Post with id {post_id} not found"}

    post.update(updated_post)
    return {"message": f"Post {id} updated", "updated_post": post}
```

**Explanation**:

- The `id` parameter identifies the post to be updated.
- The `update` method merges the existing post with the new data.

**Testing with Postman**:

1. Select the PUT method.

2. Enter the endpoint, e.g., <http://127.0.0.1:8000/posts/1>.

3. In the body, choose raw and JSON format and ensure that all the fields are included, in the update. Example:

    ```python
    {
        "title": "Updated Title",
        "content": "Updated Content",
        "published": true,
        "rating": 2
    }
    ```

4. Send the request and verify the response contains updated data.

### 4. **Delete**

- **Functionality**: Deletes a specific post by ID.
- **HTTP Method**: `DELETE`
- **Endpoint**: `/posts/{id}`

```python
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post_or_404(post_id)
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

**Explanation**:

- The `@app.delete` decorator specifies the `DELETE` method.
- The function filters out the post with the given `id`.

## FastAPI Route Ordering and Best Practices

### Why Path Parameters Should Come After Fixed Routes

- In FastAPI, route matching is performed sequentially from top to bottom.
- If a dynamic path parameter (e.g., `/posts/{post_id}`) appears before a fixed route (e.g., `/posts/latest`), the framework may mistakenly interpret the fixed route as the dynamic parameter
- For example:
  - A request to `/posts/latest` might be incorrectly routed to `/posts/{post_id}` with `post_id="latest"`.
  - This causes a type validation error because "latest" cannot be converted to an integer (if `post_id` is typed as `int`).
- In such cases, always place fixed routes like `/posts/latest` before dynamic routes such as `/posts/{post_id}` as shown below:

```python
@app.get("/posts/latest")
def get_latest_posts():
    return {"data": sorted(my_posts, key=lambda p: p["id"], reverse=True)[:2]}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Retrieves a specific post by its ID.
    """
    # Uses a generator expression to find the post with the matching ID
    post = next((p for p in my_posts if p["id"] == post_id), None)
    if not post:
        return {"error": f"Post with id {post_id} not found"}
    return {"data": post}
```

!!! Code Explanation:

- The `sorted` function is used to sort the `my_posts` list by the `id` field in descending order (`reverse=True`).
- The code then slices the first two posts using `[:2]` to return the latest two posts.
- Ensures that the posts are consistently ordered based on their creation or update timestamp (assuming `id` correlates to recency).
- Allows users to retrieve the most recent posts efficiently.

### Need for `/latest` Before `{post_id}`

- The inclusion of `/latest` as a fixed route ensures that requests specifically for the latest posts are handled before attempting to match any dynamic path parameters.
- This:
  - Prevents misinterpretation of fixed paths as dynamic parameters.
  - Makes the API more intuitive by clearly separating routes for different functionalities.

### Returning Proper HTTP Status Codes

- Use `404 Not Found` when a resource is not available (e.g., when a `post_id` does not exist).
- This can be achieved using FastAPI’s `HTTPException`:

    ```python
    from fastapi import HTTPException, status

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    ```

- For the `POST` method, we can use the status code `201` for created post:

    ```python
    @app.post("/posts", status_code=status.HTTP_201_CREATED)
    def create_post(post: Post = Body(...)):
    # --- other code goes here
    ```

- Other useful HTTP response status codes can be found [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
