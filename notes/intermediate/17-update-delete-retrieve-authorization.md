# Implementing Authorization for Update and Delete Operations

## Problem

- **Current State**:
  - The application has authentication for `delete_post` and `update_post`, but there is no check to ensure that a user can only delete or update their own posts.
  - Example: A logged-in user can delete or update any post, regardless of ownership.

## Solution: Add Ownership Checks

### 1. **Delete Post Authorization**

- **Logic**:
  - Before deleting a post, check if the logged-in user is the owner of the post.
  - If not, return a `403 Forbidden` error.
- **Implementation**:
  - Add an `if` statement to check if `post.owner_id` matches the `current_user.id`.
  - Example:

    ```python
    @router.delete(
        "/{post_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
    )
    def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
    ):
        existing_post = get_post_or_404(post_id, db)
        if existing_post.owner_id!= current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to delete this post",
            )
        db.delete(existing_post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    ```

### 2. **Update Post Authorization**

- **Logic**:
  - Before updating a post, check if the logged-in user is the owner of the post.
  - If not, return a `403 Forbidden` error.
- **Implementation**:
  - Add the same `if` statement as in `delete_post`.
  - Example:

    ```python
    @router.put("/{post_id}", response_model=PostResponse)
    def update_post(
        post_id: int,
        post: PostCreate = Body(...),
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
    ):
        existing_post = get_post_or_404(post_id, db)
        if existing_post.owner_id!= current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this post",
            )
        for key, value in post.model_dump(exclude_unset=True).items():
            setattr(existing_post, key, value)

        db.commit()
        db.refresh(existing_post)
        return existing_post
    ```

## Testing the Implementation

### 1. **Delete Post**

- **Scenario 1: User tries to delete their own post**:
  - **Action**: Delete a post owned by the logged-in user.
  - **Result**: Post is successfully deleted (`204 No Content`).
- **Scenario 2: User tries to delete another user's post**:
  - **Action**: Delete a post owned by a different user.
  - **Result**: `403 Forbidden` error with the message "Not authorized to perform requested action".

### 2. **Update Post**

- **Scenario 1: User tries to update their own post**:
  - **Action**: Update a post owned by the logged-in user.
  - **Result**: Post is successfully updated.
- **Scenario 2: User tries to update another user's post**:
  - **Action**: Update a post owned by a different user.
  - **Result**: `403 Forbidden` error with the message "Not authorized to perform requested action".

## Retrieving User-Specific Post

### Overview

- **Authenticated Routes**: Certain routes require user authentication (e.g., being logged in) to access data.
- **Data Retrieval**: Depending on the application type, you may want to retrieve data specific to the logged-in user or all users.

### Key Concepts

#### 1. **Public vs. Private Data Retrieval**

- **Private Data**: In applications like note-taking apps, users should only see their own data.
- **Public Data**: In social media apps, users can see posts from all users.

#### 2. **Filtering Data by User**

- To retrieve only the logged-in user's data, apply a filter in the query.
- Example:

     ```python
    @router.get("/", response_model=list[PostResponse])
    def get_posts(
        db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
    ):
        single_user_post = db.execute(select(Post).where(Post.owner_id == current_user.id)).scalars().all()
        return single_user_post
    ```

- **Note**: Ensure the filter uses the correct attribute (e.g., `owner_id` instead of `id`).

#### 3. **Troubleshooting Queries**

- **Debugging**: You can print the raw SQL query in the function so that when it's called it verifies the filter logic.

     ```python
     single_user_post = db.execute(select(Post).where(Post.owner_id == current_user.id)).scalars().all()
     print(single_user_post)
     ```

#### 4. **Handling Specific Post Retrieval**

- For specific posts with given IDs, we can also ensure that only the owner can retrieve their own post by implementing an exception handler:

  ```python
  @router.get("/{post_id}", response_model=PostResponse)
  def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
  ):
      existing_post = get_post_or_404(post_id, db)
      if existing_post.owner_id!= current_user.id:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Sorry, you can't access this post",
          )
      return existing_post
  ```

#### 5. **Switching Between Public and Private Data**

- **Public Data**: Since in this API we'll be implementing a public use case of a social media application, we'll remove the filter to allow all users to see all posts.
- **Private Data**: If we were to implement a private use case, then we need to add the filter to restrict data to the logged-in user.

[[TOC]]
