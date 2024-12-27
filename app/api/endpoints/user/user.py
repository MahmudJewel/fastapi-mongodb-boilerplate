# fastapi 
from fastapi import APIRouter, Depends, HTTPException
import logging
from beanie import PydanticObjectId
from typing import Annotated

# import 
from app.schemas.user import User, UserCreate, UserUpdate
from app.api.endpoints.user import functions as user_functions
from app.models import user as UserModel
from app.core.rolechecker import RoleChecker

logger = logging.getLogger(__name__)

user_module = APIRouter()

# @user_module.get('/')
# async def read_auth_page():
#     return {"msg": "Auth page Initialization done"}

@user_module.post('/')
async def create_new_user(user: UserCreate):
    existing_user = await user_functions.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = await user_functions.create_new_user(user)
    result = new_user.model_dump(exclude="password")
    return {"message": f"New user created", "data": result}

# get all user 
@user_module.get('/', 
            response_model=list[User],
            dependencies=[Depends(RoleChecker(['admin']))]
            )
async def read_all_user( skip: int = 0, limit: int = 100):
    logger.info(f"============> Getting users with skip: {skip}, limit: {limit}")
    return await user_functions.read_all_user()

# get user by id 
@user_module.get('/{user_id}', 
            # response_model=User,
            dependencies=[Depends(RoleChecker(['admin', 'user']))]
            )
async def read_user_by_id( user_id: PydanticObjectId, current_user: User = Depends(user_functions.get_current_user)):
    # logger.info(f"=======> {current_user.role.value}")
    if current_user.id == user_id or current_user.role.value == 'admin':
        user_info = await user_functions.get_user_by_id(user_id)
        result = user_info.model_dump(exclude="password")
        return result
    return {"message": "You are not allowed to see this user info"}

# update user
@user_module.patch('/{user_id}', 
            #   response_model=User,
              dependencies=[Depends(RoleChecker(['admin', 'user']))]
              )
async def update_user( 
        user_id: PydanticObjectId, 
        user: UserUpdate,
        current_user: User = Depends(user_functions.get_current_user)
    ):
    print(f"Received data: {user.model_dump()}")
    if current_user.id == user_id or current_user.role.value == 'admin':
        updated_user_info = await user_functions.update_user(user_id, user)
        result = updated_user_info.model_dump(exclude="password")
        return {"message": f"User info updated successfully", "data": result}
    return {"message": "You are not allowed to update this user info"}

# delete user
@user_module.delete('/{user_id}', 
            #    response_model=User,
               dependencies=[Depends(RoleChecker(['admin']))]
               )
async def delete_user( user_id: PydanticObjectId):
    deleted_user = await user_functions.delete_user(user_id)
    return deleted_user


