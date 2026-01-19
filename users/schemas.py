from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(5), MaxLen(100)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
