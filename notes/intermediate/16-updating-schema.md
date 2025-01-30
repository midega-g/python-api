# Updating the Application Schema

## Problem

- After adding the `owner_id` column to the `posts` table, the application started encountering issues:
  1. **Missing `owner_id` in API Responses**:
     - The `owner_id` was not being returned in the API responses when we try to get all or single post(s),  create post, and update post.
  2. **Error in `create_post`**:
     - Attempting to create a post resulted in a `500` error due to a `NULL` value in the `owner_id` column, which violates the `NOT NULL` constraint.

## Fixing the API Responses

### 1. Update the `PostResponse` Schema

- Since neither the `PostBase` or `PostResponse` schema do not include the `owner_id` field, we should add it but only to the `PostResponse` schema.
- So in `schemas.py` file, add the field to the required schema as shown below:

    ```python
    class PostResponse(PostBase):
        id: int
        owner_id: int
        created_at: datetime
    ```

### 2. Verify Changes

- After updating the schema, the `owner_id` is now included in the API responses whenever the `PostResponse` model is used.

## Fixing the `create_post` Functionality

### 1. Issue with `create_post`

- Since we don't provide an `owner_id` field to either the `PostBase` or `PostCreate` schemas, with the latter being used to create post, we get the error, `NULL value in column "owner_id" violates NOT NULL constraint`.

### 2. Solution

- **Logic**:
  - We want that the `owner_id` to be automatically set to the ID of the currently logged-in user.
  - To do so, we retrieve the user's ID from the authentication token using the `get_current_user` dependency.
- **Implementation**:
  - Update the `create_post` function to include the `owner_id` when creating a new post as follows:
  - Example:

    ```python
    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
    def create_post(
        # code ignored for brevity
        current_user: models.User = Depends(get_current_user)
    ):
        new_post = models.Post(
            **post.dict(),
            owner_id=current_user.id # include user id
        )
        # other code logic goes here
        return new_post
    ```

### 3. Testing the Fix

- **Steps**:
  1. Log in a user to retrieve an access token.
  2. Use the token to create a new post.
  3. Verify that the `owner_id` is automatically set to the logged-in user's ID.
- **Result**:
  - The `create_post` function now works without errors, and the `owner_id` is correctly set.

[[TOC]]
