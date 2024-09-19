from uuid import UUID
from typing import Annotated

from fastapi import Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca import models, repository
from src.app.core import exception
from .lca import LCA


async def get_by_id(
    lca: LCA,
    lca_component_id: UUID,
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    lca_component = await lca_component_repo.get_by_id_or_raise(id=lca_component_id)
    if lca_component.lca_id != lca.id:
        raise exception.BaseAPIError(status_code=400, detail="LCA component does not belong to the LCA")
    return lca_component


LCAComponent = Annotated[models.LCAComponent, Depends(get_by_id)]
