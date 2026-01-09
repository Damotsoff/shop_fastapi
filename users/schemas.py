from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(5), MaxLen(100)]
    email: EmailStr
