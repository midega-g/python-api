from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.models import User
from app.schemas import TokenData
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "d58d44eb67a3087ef343aee359062ea975b4984a52ed88ea58686f27ce28a524"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire_time = datetime.now(timezone.utc) + timedelta(
            minutes=expires_delta
        )
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # pylint: disable=redefined-builtin
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_token(token, credential_exception)
    user = db.query(User).filter(User.id == token.user_id).first()
    return user
