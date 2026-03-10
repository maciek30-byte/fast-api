from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Union, Annotated, Dict

from fastapi import Depends

from starlette import status

from core import oauth2_barrer

from core.seciurity import bcrypt_context
from core.settings import settings
from models import User
from jose import jwt, JWTError

def authenticate_user(username: str, password: str, db)-> Union[User, bool]:
    selected_user = db.query(User).filter(User.username == username).first()

    if not selected_user:
        return False

    if not bcrypt_context.verify(password, selected_user.hashed_password):
        return False

    return selected_user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    encode = {"sub": username, "id": user_id, "exp": datetime.now(timezone.utc) + expires_delta, "role": role}

    return jwt.encode(encode,settings.SECRET_KEY, algorithm= settings.ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_barrer)]) -> Union[Dict[str, int], None]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return {"username": username, "user_id": user_id, "user_role": user_role}

    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)




