from datetime import timedelta, datetime, timezone
from typing import Union

from core.seciurity import bcrypt_context
from core.settings import settings
from models import Users
from jose import jwt

def authenticate_user(username: str, password: str, db)-> Union[Users, bool]:
    selected_user = db.query(Users).filter(Users.username == username).first()
    if not selected_user:
        return False
    if not bcrypt_context.verify(password, selected_user.hashed_password):
        return False
    return selected_user

def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {"sub": username, "id": user_id, "exp": datetime.now(timezone.utc) + expires_delta}

    return jwt.encode(encode,settings.SECRET_KEY, algorithm= settings.ALGORITHM)
