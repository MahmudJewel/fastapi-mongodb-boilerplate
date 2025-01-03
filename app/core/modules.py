# fastapi 
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# import 
# from app.core.database import engine
# from app.core.database import user_collection
# from app.models.admin import UserAdmin
from app.api.routers.main_router import router
from app.core.settings import config

def init_routers(app_: FastAPI) -> None:
    # url path 
    app_.include_router(router)


origins = [
    "*"
]

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


# def init_cache() -> None:
#     Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

# def init_listeners(app_: FastAPI) -> None:
#     @app_.exception_handler(CustomException)
#     async def custom_exception_handler(request: Request, exc: CustomException):
#         return JSONResponse(
#             status_code=exc.code,
#             content={"error_code": exc.error_code, "message": exc.message},
#         )
