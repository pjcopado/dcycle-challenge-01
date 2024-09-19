from uuid import UUID
from typing import Annotated

from fastapi import Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca import models, repository


async def get_by_id(
    lca_id: UUID,
    lca_repo: repository.LCARepository = Depends(get_repository(repo_type=repository.LCARepository)),
):
    return await lca_repo.get_by_id_or_raise(id=lca_id)


LCA = Annotated[models.LCA, Depends(get_by_id)]
