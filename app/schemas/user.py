# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional
# from app.models.user import UserRole

# class UserBase(BaseModel):
# 	email: str

# class UserCreate(UserBase):
# 	id: str | None = None
# 	password: str
# 	# first_name: str or None = None
# 	# last_name: str or None = None
# 	id: str
# 	first_name: str | None = None
# 	last_name: str | None = None
# 	is_active: bool | None = None
# 	role: UserRole | None = UserRole.user
# 	created_at: datetime | None = None
# 	updated_at: datetime | None = None

# class UserLogin(UserBase):
# 	password: str

# class User(UserBase):
# 	id: str
# 	first_name: Optional[str]
# 	last_name: Optional[str]
# 	is_active: bool
# 	role: UserRole or None
# 	created_at: datetime
# 	updated_at: datetime
# 	class Config:
# 		from_attributes = True

# class UserUpdate(BaseModel):
# 	first_name: str or None = None
# 	last_name: str or None = None
# 	is_active: bool | None = None
# 	role: UserRole or None = None

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    role: Optional[UserRole]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


