from fastapi import FastAPI

from routers.admin import admin_router
from routers.auth import auth_router
from routers.todos import todos_router
from database import engine, Base

Base.metadata.create_all(engine)  # type: ignore[attr-defined]

app = FastAPI()

app.include_router(admin_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])















