from enum import Enum as PythonEnum
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from .common import CommonModel

class UserRole(str, PythonEnum):
    user = "user"
    admin = "admin"

class User(CommonModel):
    email: str = Field(max_length=50, unique=True)
    password: str = Field(max_length=500)
    first_name: Optional[str] = Field(max_length=50, default=None)
    last_name: Optional[str] = Field(max_length=50, default=None)
    role: UserRole = Field(default=UserRole.user)

    class Settings:
        collection = "users"
