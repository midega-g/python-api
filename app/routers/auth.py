from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.utils import verify_password
from app.models import User
from app.oauth2 import create_access_token
from app.schemas import Token
from app.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User).filter(User.email == user_credentials.username).first()
    )

    if not user or not verify_password(
        user_credentials.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
