from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos
from schemas import TodoRequest
from typing import Annotated
from database import SessionLocal, engine, Base, get_db
from starlette import status

todos_router = APIRouter()

db_dependency = Annotated[SessionLocal, Depends(get_db)]


@todos_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(db:db_dependency):
    return db.query(Todos).all()

@todos_router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_one_todo( db:db_dependency, todo_id:int = Path(gt=0),):
    to_do = db.query(Todos).filter(Todos.id == todo_id).first()
    if not to_do:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    return to_do

@todos_router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo( db:db_dependency, todo_id:int, update_request: TodoRequest):
    item: Todos = db.query(Todos).filter(Todos.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    item.title = update_request.title
    item.description = update_request.description
    item.is_completed = update_request.is_completed
    item.priority = update_request.priority

    db.add(item)
    db.commit()

@todos_router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_item(db:db_dependency, create_request: TodoRequest):
    todo_model = Todos(**create_request.model_dump())

    db.add(todo_model)
    db.commit()

@todos_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(db:db_dependency, todo_id:int = Path(gt=0),):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    db.delete(todo_model)
    db.commit()


