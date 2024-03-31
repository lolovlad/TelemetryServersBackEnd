from fastapi import APIRouter
from .login import router as login_router
from .point import router as point_router


router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(point_router)

