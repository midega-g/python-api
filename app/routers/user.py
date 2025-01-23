from fastapi import Body, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.utils import hash_password, create_new_user
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    return create_new_user(db, user.model_dump())


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id} not found",
        )
    return user
