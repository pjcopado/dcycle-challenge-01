from fastapi import APIRouter

from . import phase, lca, lca_component, source, impact

router = APIRouter()

router.include_router(router=phase.router)
router.include_router(router=lca.router)
router.include_router(router=lca_component.router)
router.include_router(router=source.router)
router.include_router(router=impact.router)
