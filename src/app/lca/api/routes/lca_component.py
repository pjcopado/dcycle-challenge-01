import typing
import uuid

from fastapi import APIRouter, Body, status, Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca.api import dependencies as deps
from src.app.lca import repository, schemas as sch
from src.app.core import exception

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
    phase_id: int = None,
    level: int | typing.Literal["last"] = None,
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    if lca_component_id is not None and (phase_id is not None or level is not None):
        raise exception.BaseAPIError(
            status_code=400, detail="Cannot filter by phase_id or level when lca_component_id is provided"
        )
    return await lca_component_repo.get_all_hierarchy(lca_id=lca.id, id=lca_component_id, phase_id=phase_id, level=level)


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
    if obj_in.parent_id is None:
        same_phase_base_lca_component = await lca_component_repo.get_by_attributes(lca_id=lca.id, phase_id=obj_in.phase_id)
        if same_phase_base_lca_component is not None:
            raise exception.BaseAPIError(status_code=400, detail="LCA base component with the same phase already exists")
    else:
        parent = await lca_component_repo.get_by_id_or_raise(obj_in.parent_id)
        if parent.lca_id != lca.id:
            raise exception.BaseAPIError(status_code=400, detail="Parent LCA component does not belong to the LCA")
        if parent.phase_id != obj_in.phase_id:
            raise exception.BaseAPIError(
                status_code=400, detail="Parent LCA component phase does not match the new component phase"
            )
        if parent.unit != obj_in.unit:
            raise exception.BaseAPIError(
                status_code=400, detail="Parent LCA component unit does not match the new component unit"
            )
    return await lca_component_repo.create(obj_in=obj_in, lca_id=lca.id)


@router.get(
    "/{lca_component_id}",
    summary="get lca component by id",
    status_code=status.HTTP_200_OK,
    response_model=sch.LCAComponentSch,
)
async def get_lca_component(lca_component: deps.LCAComponent):
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
