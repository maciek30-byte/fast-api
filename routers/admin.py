from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import  db_dependency
from models import Todo

from core.auth import get_current_user

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@admin_router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all(user_dep: user_dependency, db: db_dependency):

    if user_dep is None or user_dep.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return db.query(Todo).all()

@admin_router.delete("/todos/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(user_dep : user_dependency,todo_id: int, db: db_dependency):
    selected_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if user_dep.get('user_role') != 'admin' or selected_todo is None:
        #here we have two cases so it should be two if statement with two exceptions
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(selected_todo)
    db.commit()


