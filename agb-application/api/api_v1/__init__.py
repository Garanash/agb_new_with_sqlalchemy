from fastapi import APIRouter

from core import settings

from api.api_v1.views.users import router as users_router
from api.api_v1.views.metizes import router as metiz_router
from api.api_v1.views.RWD import router as rwd_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(users_router, prefix=settings.api.v1.users)
router.include_router(metiz_router, prefix=settings.api.v1.metiz)
router.include_router(rwd_router, prefix=settings.api.v1.RWD)
