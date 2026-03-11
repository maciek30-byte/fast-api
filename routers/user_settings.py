from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body
from starlette import status
from core.seciurity import bcrypt_context

from core.auth import get_current_user
from database import  db_dependency
from models import User
from models.password_body import PasswordUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@users_router.get("/{user_id}")
async def get_user_info(user_id: int, user: user_dependency, db:db_dependency):

    if user.get('id') != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    selected_user = db.query(User).filter(User.id == user_id).first()

    if selected_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {"first_name": selected_user.first_name, "email": selected_user.email, "role": selected_user.role }

@users_router.put("/{user_id}")
async def update_user_password(user_id: int, user: user_dependency , request_passwords: PasswordUpdate, db:db_dependency):

    if user.get('id') != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    selected_user = db.query(User).filter(User.id == user_id).first()

    if selected_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    password_verification = bcrypt_context.verify(request_passwords.current_password, selected_user.hashed_password)

    if not password_verification:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    selected_user.hashed_password = bcrypt_context.hash(request_passwords.new_password)

    db.commit()

    return {"message": "Password updated successfully"}

