# SQLAlchemy Joins in FastAPI

## Overview

- Learning how to perform joins using SQLAlchemy.
- Implementing joins in the `get_posts` route.
- Handling response validation errors with Pydantic schemas.

## Steps to Implement Joins

### Initial Query Setup

- Start by querying the `Post` model:

   ```python
   stmt = select(Post)
   ```

- Avoid executing `.all()` immediately to inspect the raw SQL.
- Print the generated SQL for debugging.

### Adding a Join with Votes Table

- Join the `Vote` table on `Post.id`:

   ```python
   stmt = stmt.outerjoin(Vote, Post.id == Vote.post_id)
   ```

- By default, SQLAlchemy uses an inner join. Explicitly make it an outer join:

   ```python
   stmt = stmt.outerjoin(Vote, Post.id == Vote.post_id)
  ```

  - **Inner Join**: Includes only rows with matching values in both tables.
  - **Outer Join**: Includes all rows from one table and matching rows from the other. Use outerjoin for this.

- Print the updated SQL query to confirm the join.

### Grouping and Counting Votes

- Group by `Post.id`:

   ```python
   stmt = stmt.group_by(Post.id)
   ```

- Count votes for each post:

   ```python
   from sqlalchemy.sql import func
   stmt = stmt.add_columns(func.count(Vote.post_id).label("votes"))
   ```

- Validate that the query correctly aggregates the vote counts.

### Handling Pydantic Validation Errors

- Errors arise because the response model does not match the new structure.
- Define a new response schema `PostWithVotes`:

    ```python
    class PostWithVotes(BaseModel):
        Post: PostResponse
        votes: int
    ```

- Ensure `Post` field in the schema is capitalized (`Post` instead of `post`).
- Update the response model in the `get_posts` function:

    ```python
    @router.get("/", response_model=list[PostWithVotes])
    ```

### Restoring Filters

- Reintroduce search filters before executing the query:

    ```python
    stmt = stmt.where(Post.title.contains(search))
    ```

- Implement pagination using `limit` and `skip`:

    ```python
    stmt = stmt.offset(skip).limit(limit)
    ```

- Execute the final query and return results:

    ```python
    results = db.execute(stmt).all()
    return results
    ```

## Updating the Get Single Post Route

- Modify the `get_post` function to include the vote count:

    ```python
    stmt = select(Post).outerjoin(Vote, Post.id == Vote.post_id).group_by(Post.id)
    stmt = stmt.add_columns(func.count(Vote.post_id).label("votes"))
    stmt = stmt.where(Post.id == post_id)
    ```

- Ensure the response model reflects the new structure:

    ```python
    @router.get("/{post_id}", response_model=PostWithVotes)
    ```

- Debug and verify the output to ensure votes are included.

## Considering Create & Update Routes

- Decide whether to include vote counts in `create_post` and `update_post`:
  - These typically return only the created/updated post details.
  - Adding votes in these responses is unnecessary and complex.
  - Focus on retrieving votes in `get` operations instead.

## Debugging Tips

- If validation errors persist, ensure that the schema field names match the query output.
- Restart the application if unexpected behavior occurs.
- Use `print(results)` to inspect the returned data structure.

[[TOC]]
