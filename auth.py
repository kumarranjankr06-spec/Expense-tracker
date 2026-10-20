import bcrypt

import os
import jwt

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User

# Set SECRET_KEY in your environment before running the app.
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    current_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if current_user is None:
        raise credentials_exception

    return current_user


def hash_password(password: str) -> str:

  password_bytes = password.encode("utf-8")

  salt = bcrypt.gensalt()

  hashed = bcrypt.hashpw(password_bytes,salt)

  return hashed.decode("utf-8")


def verify_password(plain_password: str, stored_hash: str) -> bool:
    
    password_bytes = plain_password.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")
    
    
    return bcrypt.checkpw(password_bytes, hash_bytes)