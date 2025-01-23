from fastapi import Body, Depends, Response, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.utils import get_post_or_404
from app.models import Post
from app.schemas import PostCreate, PostResponse
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
def create_post(post: PostCreate = Body(...), db: Session = Depends(get_db)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.execute(select(Post)).scalars().all()
    return all_posts


@router.get("/latest/{count_}", response_model=list[PostResponse])
def get_latest_posts(count_: int, db: Session = Depends(get_db)):
    latest_posts = (
        db.execute(select(Post).order_by(Post.created_at.desc()).limit(count_))
        .scalars()
        .all()
    )
    return latest_posts


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_or_404(post_id, db)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, post: PostCreate = Body(...), db: Session = Depends(get_db)
):
    existing_post = get_post_or_404(post_id, db)

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
def delete_post(post_id: int, db: Session = Depends(get_db)):
    existing_post = get_post_or_404(post_id, db)
    db.delete(existing_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
