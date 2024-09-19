import uuid

from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca.api import dependencies as deps
from src.app.lca import repository, schemas as sch

router = APIRouter(prefix="/lca/{lca_id}/components", tags=["lca components"])


@router.get(
    "",
    summary="list lca components",
    status_code=status.HTTP_200_OK,
    response_model=list[sch.LCAComponentHierarchySch],
)
async def list_lca_components(
    lca: deps.LCA,
    lca_component_id: uuid.UUID = None,
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    return await lca_component_repo.get_all_hierarchy(lca_id=lca.id, id=lca_component_id)


@router.post(
    "",
    summary="create lca component",
    status_code=status.HTTP_201_CREATED,
    response_model=sch.LCAComponentHierarchySch,
)
async def create_lca_component(
    lca: deps.LCA,
    obj_in: sch.LCAComponentCreateSch = Body(...),
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    return await lca_component_repo.create(obj_in=obj_in, lca_id=lca.id)


@router.get(
    "/{lca_component_id}",
    summary="get lca component by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.LCAComponentSch,
)
async def get_lca_component(lca_component: deps.LCAComponent, lca: deps.LCA):
    return lca_component


@router.put(
    "/{lca_component_id}",
    summary="update lca component by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.LCAComponentSch,
)
async def update_lca_component(
    lca_component: deps.LCAComponent,
    obj_in: sch.LCAComponentUpdateSch = Body(...),
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    return await lca_component_repo.update(obj_db=lca_component, obj_in=obj_in)


@router.delete(
    "/{lca_component_id}",
    summary="delete lca component by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_lca_component(
    lca_component: deps.LCAComponent,
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    await lca_component_repo.delete(obj_db=lca_component)
