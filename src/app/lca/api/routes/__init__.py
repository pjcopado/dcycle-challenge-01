from fastapi import APIRouter

from . import phase, lca, lca_component

router = APIRouter()

router.include_router(router=phase.router)
router.include_router(router=lca.router)
router.include_router(router=lca_component.router)
