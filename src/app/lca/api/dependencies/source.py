from uuid import UUID
from typing import Annotated

from fastapi import Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.lca import models, repository


async def get_by_id(
    source_id: UUID,
    source_repo: repository.SourceRepository = Depends(get_repository(repo_type=repository.SourceRepository)),
):
    return await source_repo.get_by_id_or_raise(id=source_id)


Source = Annotated[models.Source, Depends(get_by_id)]
