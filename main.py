from fastapi import FastAPI
from routers.auth import auth_router
from routers.todos import todos_router
from database import engine, Base
from models import Todo, User  # Import models to register them with Base

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])















