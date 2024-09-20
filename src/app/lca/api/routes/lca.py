from fastapi import APIRouter, Body, status, Depends, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca.api import dependencies as deps
from src.app.lca import repository, schemas as sch

router = APIRouter(prefix="/lca", tags=["lca"])


@router.get(
    "",
    summary="list lca",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.LCASch],
)
async def list_lca(
    name: str = Query(None, min_length=2),
    lca_repo: repository.LCARepository = Depends(get_repository(repo_type=repository.LCARepository)),
):
    stmt = await lca_repo.get_all_stmt(name=name)
    return await sqla_paginate(lca_repo.async_session, stmt)


@router.post(
    "",
    summary="create lca",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.LCASch,
)
async def create_lca(
    obj_in: sch.LCACreateSch = Body(...),
    lca_repo: repository.LCARepository = Depends(get_repository(repo_type=repository.LCARepository)),
):
    return await lca_repo.create(obj_in=obj_in)


@router.get(
    "/{lca_id}",
    summary="get lca by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.LCASch,
)
async def get_lca(
    lca: deps.LCA,
):
    return lca


@router.put(
    "/{lca_id}",
    summary="update lca by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.LCASch,
)
async def update_lca(
    lca: deps.LCA,
    obj_in: sch.LCAUpdateSch = Body(...),
    lca_repo: repository.LCARepository = Depends(get_repository(repo_type=repository.LCARepository)),
):
    return await lca_repo.update(obj_db=lca, obj_in=obj_in)


@router.delete(
    "/{lca_id}",
    summary="delete lca by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_lca(
    lca: deps.LCA,
    lca_repo: repository.LCARepository = Depends(get_repository(repo_type=repository.LCARepository)),
):
    await lca_repo.delete(obj_db=lca)


@router.get(
    "/{lca_id}/impacts",
    summary="get impacts by lca id",
    status_code=status.HTTP_200_OK,
    response_model=list[sch.LCAImpactSch],
)
async def get_lca(
    lca: deps.LCA,
    lca_repo: repository.LCARepository = Depends(get_repository(repo_type=repository.LCARepository)),
):
    return await lca_repo.calculate_impact(id=lca.id)
