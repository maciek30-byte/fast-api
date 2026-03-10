from fastapi import APIRouter

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@users_router.get("/users/{id}")
async def get_user_info():
    return {"id": id}

@users_router.put("/users/{id}")
async def update_user_password(id: int, password: str):
    return {"id": id, "password": password}