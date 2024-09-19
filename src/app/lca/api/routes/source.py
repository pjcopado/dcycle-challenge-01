from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca.api import dependencies as deps
from src.app.lca import repository, schemas as sch

router = APIRouter(prefix="/source", tags=["source"])


@router.get(
    "",
    summary="list source",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.SourceSch],
)
async def list_source(
    source_repo: repository.SourceRepository = Depends(get_repository(repo_type=repository.SourceRepository)),
):
    stmt = await source_repo.get_all_stmt()
    return await sqla_paginate(source_repo.async_session, stmt)


@router.post(
    "",
    summary="create source",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.SourceSch,
)
async def create_source(
    obj_in: sch.SourceCreateSch = Body(...),
    source_repo: repository.SourceRepository = Depends(get_repository(repo_type=repository.SourceRepository)),
):
    return await source_repo.create(obj_in=obj_in)


@router.get(
    "/{source_id}",
    summary="get source by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.SourceSch,
)
async def get_source(
    source: deps.Source,
):
    return source


@router.put(
    "/{source_id}",
    summary="update source by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.SourceSch,
)
async def update_source(
    source: deps.Source,
    obj_in: sch.SourceUpdateSch = Body(...),
    source_repo: repository.SourceRepository = Depends(get_repository(repo_type=repository.SourceRepository)),
):
    return await source_repo.update(obj_db=source, obj_in=obj_in)


@router.delete(
    "/{source_id}",
    summary="delete source by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_source(
    source: deps.Source,
    source_repo: repository.SourceRepository = Depends(get_repository(repo_type=repository.SourceRepository)),
):
    await source_repo.delete(obj_db=source)
