from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.utils import get_post_or_404
from app.models import Vote
from app.oauth2 import get_current_user
from app.schemas import VoteSchema
from app.database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


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

    # Check if the post exists using the utility function
    get_post_or_404(vote_data.post_id, db)

    # Check if the user has already voted on the post
    vote_query = db.execute(
        select(Vote).where(
            Vote.post_id == vote_data.post_id,
            Vote.user_id == current_user.id,
        )
    )
    existing_vote: Vote | None = vote_query.scalars().first()

    if vote_data.vote_direction == 1:
        # User is trying to vote
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote_data.post_id}.",
            )
        # Create a new vote
        new_vote = Vote(post_id=vote_data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote."}

    # User is trying to remove their vote
    if not existing_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.id} has not voted on post {vote_data.post_id}.",
        )
    # Delete the existing vote
    db.delete(existing_vote)
    db.commit()
    return {"message": "Successfully removed vote."}
