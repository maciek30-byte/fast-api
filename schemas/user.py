from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=3)
    is_active: bool = Field(default=True)
    role: str = Field(min_length=3)
