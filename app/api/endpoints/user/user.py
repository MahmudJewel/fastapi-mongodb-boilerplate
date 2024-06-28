# fastapi 
from fastapi import APIRouter, Depends, HTTPException

# import 
from app.schemas.user import User, UserCreate, UserUpdate
from app.api.endpoints.user import functions as user_functions
from app.models import user as UserModel

user_module = APIRouter()

# @user_module.get('/')
# async def read_auth_page():
#     return {"msg": "Auth page Initialization done"}

@user_module.post('/', response_model=User)
async def create_new_user(user: UserCreate):
    existing_user = await user_functions.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = await user_functions.create_new_user(user)
    return new_user

# get all user 
@user_module.get('/', 
            response_model=list[User],
            # dependencies=[Depends(RoleChecker(['admin']))]
            )
async def read_all_user( skip: int = 0, limit: int = 100):
    return await user_functions.read_all_user()

# get user by id 
@user_module.get('/{user_id}', 
            response_model=User,
            # dependencies=[Depends(RoleChecker(['admin']))]
            )
async def read_user_by_id( user_id: str):
    return await user_functions.get_user_by_id(user_id)

# update user
@user_module.patch('/{user_id}', 
              response_model=User,
            #   dependencies=[Depends(RoleChecker(['admin']))]
              )
async def update_user( user_id: str, user: UserUpdate):
    print(f"Received data: {user.model_dump()}")
    return await user_functions.update_user(user_id, user)

# delete user
@user_module.delete('/{user_id}', 
            #    response_model=User,
            #    dependencies=[Depends(RoleChecker(['admin']))]
               )
async def delete_user( user_id: str):
    deleted_user = await user_functions.delete_user(user_id)
    return deleted_user


