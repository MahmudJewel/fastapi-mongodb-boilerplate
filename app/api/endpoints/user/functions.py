from fastapi import HTTPException, status, Depends
from typing import Annotated
from datetime import datetime, timedelta, timezone

# # from sqlalchemy.orm import Session

# from auth import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt

# # import 
from app.models import user as UserModel
from app.schemas.user import UserCreate, UserUpdate, User
from app.core.settings import SECRET_KEY, ALGORITHM
# from app.core.dependencies import get_db, oauth2_scheme

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# get user by email 
async def get_user_by_email(email: str):
    return await UserModel.User.find_one(UserModel.User.email == email)

# get user by id
def get_user_by_id(user_id: str):
    db_user = UserModel.User.find_one(UserModel.User.id == user_id)
    # print('==========================>', db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# crete new user 
async def create_new_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel.User(email=user.email, password=hashed_password, first_name=user.first_name, last_name=user.last_name)
    # new_user = UserModel.User(**user.model_dump())
    await new_user.insert()
    return new_user
    


# get all user 
async def read_all_user():
    users = await UserModel.User.find_all().to_list()
    return users

# # update user
# def update_user(db: Session, user_id: int, user: UserUpdate):
#     db_user = get_user_by_id(db, user_id)
#     updated_data = user.model_dump(exclude_unset=True) # partial update
#     for key, value in updated_data.items():
#         setattr(db_user, key, value)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # delete user
# def delete_user(db: Session, user_id: str):
#     db_user = get_user_by_id(db, user_id)
#     db.delete(db_user)
#     db.commit()
#     # db.refresh(db_user)
#     return {"msg": f"{db_user.email} deleted successfully"}

# # =====================> login/logout <============================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(user: UserCreate):
    member = await get_user_by_email(email=user.email)
    print("authenticate_user ======>", member, member.email)
    # if not member:
    #     return False
    # if not verify_password(user.password, member.password):
    #     return False
    return member

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# # get current users info 
# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid authentication credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # print(f"Payload =====> {payload}")
#         current_email: str = payload.get("email")
#         if current_email is None:
#             raise credentials_exception
#         user = get_user_by_email(db, current_email)
#         if user is None:
#             raise credentials_exception
#         return user
#     except JWTError:
#         raise credentials_exception

