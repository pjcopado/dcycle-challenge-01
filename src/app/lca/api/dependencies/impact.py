from uuid import UUID
from typing import Annotated

from fastapi import Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca import models, repository


async def get_by_id(
    impact_id: UUID,
    impact_repo: repository.ImpactRepository = Depends(get_repository(repo_type=repository.ImpactRepository)),
):
    return await impact_repo.get_by_id_or_raise(id=impact_id)


Impact = Annotated[models.Impact, Depends(get_by_id)]
