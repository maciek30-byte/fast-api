from typing import Annotated

from fastapi import HTTPException, Path, APIRouter, Depends

from schemas import TodoRequest
from database import  db_dependency
from starlette import status
from services.auth import get_current_user
from services.todo_service import TodoService

todos_router = APIRouter(
    dependencies=[Depends(get_current_user)],
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@todos_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(user_dep: user_dependency, db:db_dependency):
    todo_service = TodoService(db)

    return todo_service.get_all(user_dep.get("user_id"))


@todos_router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_one_todo(user_dep: user_dependency, db:db_dependency, todo_id:int = Path(gt=0),):
    todo_service = TodoService(db)
    to_do_item = todo_service.get_by_id(todo_id, user_dep.get("user_id"))

    if not to_do_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    return to_do_item

@todos_router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user_dep : user_dependency, db:db_dependency, todo_id:int, update_request: TodoRequest):
    todo_service = TodoService(db)
    item = todo_service.update(user_dep.get("user_id"), update_request, todo_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    return item

@todos_router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_item(db:db_dependency, create_request: TodoRequest, user_dep: user_dependency):
    todo_service = TodoService(db)

    todo_service.create(create_request, user_dep.get("user_id"))

@todos_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(user_dep: user_dependency,db:db_dependency, todo_id:int = Path(gt=0),):
    todo_service = TodoService(db)

    item = todo_service.delete(user_dep.get("user_id"), todo_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    return item


