from uuid import UUID
from typing import Annotated

from fastapi import Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca import models, repository


async def get_by_id(
    lca_component_id: UUID,
    lca_component_repo: repository.LCAComponentRepository = Depends(get_repository(repo_type=repository.LCAComponentRepository)),
):
    return await lca_component_repo.get_by_id_or_raise(id=lca_component_id)


LCAComponent = Annotated[models.LCAComponent, Depends(get_by_id)]
