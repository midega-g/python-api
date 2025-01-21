from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Post


def get_post_or_404(post_id: int, db: Session):
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found.",
        )
    return post
