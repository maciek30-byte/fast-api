from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from exceptions import UserNotFoundError, InvalidPasswordError
from services import UserSettingsService

from core.auth import get_current_user
from database import  db_dependency
from models.password_body import PasswordUpdateRequest


users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@users_router.get("/{user_id}")
async def get_user_info(user_id: int, user: user_dependency, db:db_dependency):

    if user.get('id') != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        return UserSettingsService(db).get_user_info(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@users_router.put("/{user_id}")
async def update_user_password(user_id: int, user: user_dependency, request_passwords: PasswordUpdateRequest, db:db_dependency):

    if user.get('id') != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    try:
        return UserSettingsService(db).update_password(user_id, request_passwords)
    except UserNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except InvalidPasswordError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

