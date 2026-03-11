from typing import Annotated

from pydantic import BaseModel, Field


class PasswordUpdateRequest(BaseModel):
    current_password: Annotated[str, Field(min_length=3)]
    new_password: Annotated[str, Field(min_length=3)]