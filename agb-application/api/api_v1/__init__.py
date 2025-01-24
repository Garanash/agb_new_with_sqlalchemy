from fastapi import APIRouter

from core import settings

from .users import router as users_router
from .metizes import router as metiz_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(users_router, prefix=settings.api.v1.users)
router.include_router(metiz_router, prefix=settings.api.v1.metiz)