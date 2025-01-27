from fastapi import APIRouter

from core import settings

from api.api_v1.views.users import router as users_router
from api.api_v1.views.metizes import router as metiz_router
from api.api_v1.views.RWD import router as rwd_router
from api.api_v1.views.project import router as project_router
from api.api_v1.views.purchased import router as purchased_router
from api.api_v1.views.purchasedhydroperforator import router as purchasedhydroperforator_router
from api.api_v1.views.adapters_and_plugs import router as adapterandplugs_router
from api.api_v1.views.according_to_the_draw import router as according_to_the_draw_router
from api.api_v1.views.search import router as search_router

router = APIRouter(
    # prefix=settings.api.v1.prefix
)
router.include_router(users_router, prefix=settings.api.v1.users)
router.include_router(metiz_router, prefix=settings.api.v1.metiz)
router.include_router(rwd_router, prefix=settings.api.v1.RWD)
router.include_router(project_router, prefix=settings.api.v1.project)

router.include_router(purchased_router, prefix=settings.api.v1.purchased)
router.include_router(purchasedhydroperforator_router, prefix=settings.api.v1.purchasedHydro)
router.include_router(adapterandplugs_router, prefix=settings.api.v1.adaptersAndPlugs)
router.include_router(according_to_the_draw_router, prefix=settings.api.v1.according)

router.include_router(search_router)