from typing import List
from models import Todo
from schemas import TodoRequest


class TodoService:
    def __init__(self, db ):
        self.db = db

    def get_all(self, owner_id: int)->List[Todo]:
        return self.db.query(Todo).filter(Todo.owner_id == owner_id).all()

    def get_by_id(self, todo_id: int, user_id: int):
        return  self.db.query(Todo).filter(
            Todo.owner_id == user_id,
            Todo.id == todo_id
        ).first()


    def create(self, data: TodoRequest, owner_id: int):
        new_todo = Todo(**{**data.model_dump(), "owner_id": owner_id})

        self.db.add(new_todo)
        self.db.commit()

    def update(self, user_id: int, data: TodoRequest, id_to_update: int):
        item: Todo = self.db.query(Todo).filter(
            Todo.owner_id == user_id,
            Todo.id == id_to_update
        ).first()

        if not item:
            return None

        item.title = data.title  # type: ignore
        item.description = data.description  # type: ignore
        item.is_completed = data.is_completed  # type: ignore
        item.priority = data.priority  # type: ignore

        self.db.add(item)
        self.db.commit()

        return item

    def delete(self, user_id: int, id_to_delete: int):
        selected_todo = self.db.query(Todo).filter(
            Todo.owner_id == user_id,
            Todo.id == id_to_delete
        ).first()

        if not selected_todo:
            return None

        self.db.delete(selected_todo)
        self.db.commit()

        return selected_todo







