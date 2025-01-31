
# Voting System Logic

## Overview

The voting system allows users to like or remove a like from a post. The logic is implemented in a FastAPI route, with the following key features:

- **Path**: `/vote`
- **HTTP Method**: `POST`
- **Authentication**: Requires a valid JWT token.
- **Request Body**:
  - `post_id`: The ID of the post to vote on.
  - `vote_direction`: `1` to like, `0` to remove a like.

## Schema Definition

The `VoteSchema` is defined in `models.py` as follows:

```python
from pydantic import BaseModel, Field
from typing import Annotated

class VoteSchema(BaseModel):
    post_id: int
    vote_direction: Annotated[int, Field(ge=0, le=1)]
```

- `post_id`: The ID of the post to vote on.
- `vote_direction`: Must be `0` (remove like) or `1` (add like).

## Router Setup

The voting logic is implemented in a FastAPI router, `vote.py`, setup as follows:

### Imports

```python
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.models import Vote, Post
from app.oauth2 import get_current_user
from app.schemas import VoteSchema
from app.database import get_db
from app.utils import get_post_or_404
```

### Router Configuration

```python
router = APIRouter(prefix="/vote", tags=["Vote"])
```

### Endpoint Logic

The `/vote` endpoint handles two main actions:

1. **Adding a vote** (`vote_direction == 1`).
2. **Removing a vote** (`vote_direction == 0`).

```python
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote_data: VoteSchema,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    """
    Endpoint to handle voting on a post.
    - If `vote_data.vote_direction == 1`, adds a vote.
    - If `vote_data.vote_direction == 0`, removes an existing vote.
    """
```

#### Step 1: Check if the Post Exists

Before processing the vote, ensure the post exists using the `get_post_or_404` utility function:

```python
get_post_or_404(vote_data.post_id, db)
```

#### Step 2: Check if the User Has Already Voted

Query the database to see if the user has already voted on the post:

```python
vote_query = db.execute(
    select(Vote).where(
        Vote.post_id == vote_data.post_id,
        Vote.user_id == current_user.id,
    )
)
existing_vote: Vote | None = vote_query.scalars().first()
```

#### Step 3: Handle Adding a Vote (`vote_direction == 1`)

If the user wants to add a vote:

1. Check if the user has already voted.
2. If not, create a new vote and save it to the database.

```python
if vote_data.vote_direction == 1:
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id} has already voted on post {vote_data.post_id}.",
        )
    new_vote = Vote(post_id=vote_data.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "Successfully added vote."}
```

#### Step 4: Handle Removing a Vote (`vote_direction == 0`)

If the user wants to remove a vote:

1. Check if the vote exists.
2. If it exists, delete the vote from the database.

```python
if not existing_vote:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {current_user.id} has not voted on post {vote_data.post_id}.",
    )
db.delete(existing_vote)
db.commit()
return {"message": "Successfully removed vote."}
```

## Testing the Endpoint

### Test Cases

1. **Add a Vote**:
   - **Request**:

     ```json
     POST /vote/
     {
       "post_id": 10,
       "vote_direction": 1
     }
     ```

   - **Response**:

     ```json
     {
       "message": "Successfully added vote."
     }
     ```

2. **Remove a Vote**:
   - **Request**:

     ```json
     POST /vote/
     {
       "post_id": 10,
       "vote_direction": 0
     }
     ```

   - **Response**:

     ```json
     {
       "message": "Successfully removed vote."
     }
     ```

3. **Post Not Found**:
   - **Response**:

     ```json
     {
       "detail": "Post with id 10 was not found."
     }
     ```

4. **User Tries to Vote Twice**:
   - **Response**:

     ```json
     {
       "detail": "User 24 has already voted on post 10."
     }
     ```

5. **User Tries to Remove a Non-Existent Vote**:
   - **Response**:

     ```json
     {
       "detail": "User 24 has not voted on post 10."
     }
     ```

## Notes

- **Authentication**: The user ID is extracted from the JWT token, so it doesn't need to be included in the request body.
- **Validation**: The `vote_direction` field is validated to ensure it's either `0` or `1`.
- **Error Handling**: Proper error messages and status codes are returned for invalid requests.
