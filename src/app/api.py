from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.app.core.config import settings
from src.app.common.api.routes import router as common_router
from src.app.lca.api.routes import router as lca_router


router = APIRouter()


@router.get("/", include_in_schema=False)
def docs():
    return RedirectResponse(url="/docs")


router.include_router(prefix=settings.API_V1_STR, router=common_router)
router.include_router(prefix=settings.API_V1_STR, router=lca_router)
