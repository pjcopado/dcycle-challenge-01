from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca.api import dependencies as deps
from src.app.lca import repository, schemas as sch

router = APIRouter(prefix="/phase-groups", tags=["phases"])


@router.get(
    "",
    summary="list phase groups",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.PhaseGroupSch],
)
async def list_phases(
    phase_repo: repository.PhaseGroupRepository = Depends(get_repository(repo_type=repository.PhaseGroupRepository)),
):
    stmt = await phase_repo.get_all_stmt()
    return await sqla_paginate(phase_repo.async_session, stmt)
