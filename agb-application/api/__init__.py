from fastapi import APIRouter

from core import settings

from .api_v1 import router as apiv1_router

router = APIRouter()
router.include_router(apiv1_router, prefix="/u1")
