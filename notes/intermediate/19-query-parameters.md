# Query Parameters in APIs

## Introduction to Query Parameters

1. **What Are Query Parameters?**
   - Query parameters are optional key-value pairs that appear in the URL after a `?`.
   - They are used to filter, sort, or paginate data returned by an API.
   - Example: `https://example.com/search?location=miami&limit=10`

2. **Common Use Cases**:
   - Filtering results (e.g., posts created in the last 2 hours).
   - Pagination (e.g., retrieving posts 20 at a time).
   - Searching (e.g., finding posts with specific keywords).

3. **Example from Yelp**:
   - URL: `https://www.yelp.com/search?find_loc=Miami+Florida`
   - `find_loc` is a query parameter that filters results by location.

## Implementing Query Parameters in FastAPI

### 1. **Limiting Results**

- Allow users to specify how many results they want to retrieve.
- Example: `limit=10` retrieves 10 posts.

   **Implementation**:

   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/posts")
   def get_posts(limit: int = 10):
       print(limit)  # Print the limit for debugging
       # Query the database with the limit
       posts = db.execute(select(Post).limit(limit)).scalars().all()
       return posts
   ```

   **Usage**:

- URL: `/posts?limit=3` retrieves 3 posts.

### 2. **Skipping Results (Pagination)**

- Allow users to skip a certain number of results.
- Example: `skip=2` skips the first 2 posts.

   **Implementation**:

   ```python
   @app.get("/posts")
   def get_posts(limit: int = 10, skip: int = 0):
       # Query the database with limit and offset
       posts = db.execute(select(Post).offset(skip).limit(limit)).scalars().all()
       return posts
   ```

   **Usage**:

- URL: `/posts?limit=2&skip=2` retrieves 2 posts, skipping the first 2.

### 3. **Search Functionality**

- Allow users to search for posts by keywords in the title.
- Example: `search=beaches` retrieves posts with "beaches" in the title.

   **Implementation**:

   ```python
   from typing import Optional

   @app.get("/posts")
   def get_posts(limit: int = 10, skip: int = 0, search: Optional[str] = ""):
       # Query the database with search functionality
       posts = db.execute(select(Post).where(Post.title.contains(search)).offset(skip).limit(limit)).scalars().all()
       return posts
   ```

   **Usage**:

- URL: `/posts?search=beaches` retrieves posts with "beaches" in the title.
- URL: `/posts?search=something%20beaches` retrieves posts with "something beaches" in the title (using `%20` for spaces).

### Combining Query Parameters

- Multiple query parameters can be combined for advanced filtering.
- Example: `/posts?limit=2&skip=1&search=beaches`
  - Retrieves 2 posts, skips the first post, and filters by "beaches" in the title.

!!! Best Practicesmwam

- Provide default values for optional parameters.
- Use `Optional` for parameters that may not always be provided.
- Handle spaces in search queries using `%20`.
- Be mindful of database performance when using `filter` and `contains` on large datasets.
- Consider indexing columns used in search queries.
- Test query parameters thoroughly to ensure they work as expected.
- Example: Test edge cases like empty search strings or large skip values.

[[TOC]]
