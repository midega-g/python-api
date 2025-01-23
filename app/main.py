from fastapi import Body, Depends, FastAPI, Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from .utils import hash_password, create_new_user, get_post_or_404
from .models import Base, Post, User
from .schemas import PostCreate, UserCreate, PostResponse, UserResponse
from .database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
def create_post(post: PostCreate = Body(...), db: Session = Depends(get_db)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.execute(select(Post)).scalars().all()
    return all_posts


@app.get("/posts/latest/{count_}", response_model=list[PostResponse])
def get_latest_posts(count_: int, db: Session = Depends(get_db)):
    latest_posts = (
        db.execute(select(Post).order_by(Post.created_at.desc()).limit(count_))
        .scalars()
        .all()
    )
    return latest_posts


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_or_404(post_id, db)


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, post: PostCreate = Body(...), db: Session = Depends(get_db)
):
    existing_post = get_post_or_404(post_id, db)

    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(existing_post, key, value)

    db.commit()
    db.refresh(existing_post)
    return existing_post


@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    existing_post = get_post_or_404(post_id, db)
    db.delete(existing_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    return create_new_user(db, user.model_dump())


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with {user_id} not found",
        )
    return user
