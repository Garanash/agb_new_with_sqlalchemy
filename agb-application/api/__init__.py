from fastapi import APIRouter

from api.api_v1 import router as apiv1_router

router = APIRouter()
router.include_router(apiv1_router)
