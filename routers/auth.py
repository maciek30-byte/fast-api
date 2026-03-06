from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.seciurity import bcrypt_context
from database import  db_dependency
from models import User
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from schemas import CreateUserRequest
from schemas.token import Token
from services.auth import authenticate_user, create_access_token

auth_router = APIRouter()
@auth_router.post('/token', status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    token = create_access_token(authenticated_user.username, authenticated_user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
@auth_router.get("/users",status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    return db.query(User).all()

@auth_router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=create_user_request.is_active,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    db.add(create_user_model)
    db.commit()