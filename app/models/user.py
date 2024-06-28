# from beanie import Document, Link
# from pydantic import BaseModel, Field, EmailStr
# from typing import List, Optional
# from enum import Enum
# from app.models.common import CommonModel

# class UserRole(str, Enum):
#     user = "user"
#     admin = "admin"

# class User(CommonModel):
#     email: EmailStr
#     password: str
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     role: UserRole = UserRole.user
#     # bookings: List[Link["Booking"]] = Field(default_factory=list)

#     class Settings:
#         collection = "users"

#     def __repr__(self):
#         return f"{self.email}"

# user.py
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
