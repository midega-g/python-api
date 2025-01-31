# pylint: disable=not-callable

from fastapi import (
    Body,
    Query,
    Depends,
    Response,
    APIRouter,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from app.utils import get_post_or_404
from app.models import Post, Vote
from app.oauth2 import get_current_user
from app.schemas import PostCreate, PostResponse, PostWithVotes
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
def create_post(
    post: PostCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_post = Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/", response_model=list[PostResponse])
@router.get("/", response_model=list[PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = Query(default=""),
):  # pylint: disable=unused-argument
    stmt = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .outerjoin(Vote, Post.id == Vote.post_id)
        .where(Post.title.contains(search))
        .group_by(Post.id)
        .offset(skip)
        .limit(limit)
    )
    results = db.execute(stmt).all()
    return results


@router.get("/latest/{count_}", response_model=list[PostResponse])
def get_latest_posts(
    count_: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):  # pylint: disable=unused-argument
    latest_posts = (
        db.execute(select(Post).order_by(Post.created_at.desc()).limit(count_))
        .scalars()
        .all()
    )
    return latest_posts


@router.get("/{post_id}", response_model=PostWithVotes)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):  # pylint: disable=unused-argument

    get_post_or_404(post_id, db)
    stmt = (
        select(Post)
        .outerjoin(Vote, Post.id == Vote.post_id)
        .group_by(Post.id)
        .add_columns(func.count(Vote.post_id).label("votes"))
        .where(Post.id == post_id)
    )
    print(stmt)
    return db.execute(stmt).first()


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing_post = get_post_or_404(post_id, db)
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post",
        )
    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(existing_post, key, value)

    db.commit()
    db.refresh(existing_post)
    return existing_post


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
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post",
        )
    db.delete(existing_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
