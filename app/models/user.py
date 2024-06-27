from beanie import Document, Link
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum
from app.models.common import CommonModel

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class User(CommonModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.user
    # bookings: List[Link["Booking"]] = Field(default_factory=list)

    class Settings:
        collection = "users"

    def __repr__(self):
        return f"{self.email}"
