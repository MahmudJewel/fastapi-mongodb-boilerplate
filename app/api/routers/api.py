from fastapi import APIRouter
from app.api.routers.user import user_router
from app.core.database import db_module
router = APIRouter()

router.include_router(db_module)
router.include_router(user_router)

# from fastapi import APIRouter
# from app.api.routers.user import user_router
# from app.core.database import init

# # Initialize the main API router
# router = APIRouter()

# # Initialize the database connection during startup
# async def startup():
#     await init()

# # Include sub-routers
# router.include_router(user_router)

# # Pass startup logic to the application lifespan
# def get_lifespan():
#     from contextlib import asynccontextmanager
#     from fastapi import FastAPI

#     @asynccontextmanager
#     async def lifespan(app: FastAPI):
#         await startup()
#         yield

#     return lifespan

