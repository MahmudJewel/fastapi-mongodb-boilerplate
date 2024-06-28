from fastapi import APIRouter
from app.api.routers.user import user_router
from app.core.database import db_module
router = APIRouter()

router.include_router(db_module)
router.include_router(user_router)


