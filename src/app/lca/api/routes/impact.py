from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca.api import dependencies as deps
from src.app.lca import repository, schemas as sch

router = APIRouter(prefix="/impact", tags=["impact"])


@router.get(
    "",
    summary="list impact",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.ImpactSch],
)
async def list_impact(
    impact_repo: repository.ImpactRepository = Depends(get_repository(repo_type=repository.ImpactRepository)),
):
    stmt = await impact_repo.get_all_stmt()
    return await sqla_paginate(impact_repo.async_session, stmt)


@router.post(
    "",
    summary="create impact",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.ImpactSch,
)
async def create_impact(
    obj_in: sch.ImpactCreateSch = Body(...),
    impact_repo: repository.ImpactRepository = Depends(get_repository(repo_type=repository.ImpactRepository)),
):
    return await impact_repo.create(obj_in=obj_in)


@router.get(
    "/{impact_id}",
    summary="get impact by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.ImpactSch,
)
async def get_impact(
    impact: deps.Impact,
):
    return impact


@router.put(
    "/{impact_id}",
    summary="update impact by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.ImpactSch,
)
async def update_impact(
    impact: deps.Impact,
    obj_in: sch.ImpactUpdateSch = Body(...),
    impact_repo: repository.ImpactRepository = Depends(get_repository(repo_type=repository.ImpactRepository)),
):
    return await impact_repo.update(obj_db=impact, obj_in=obj_in)


@router.delete(
    "/{impact_id}",
    summary="delete impact by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_impact(
    impact: deps.Impact,
    impact_repo: repository.ImpactRepository = Depends(get_repository(repo_type=repository.ImpactRepository)),
):
    await impact_repo.delete(obj_db=impact)
