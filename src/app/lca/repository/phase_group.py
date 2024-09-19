import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from src.app.common.repository import BaseRepository
from src.app.lca import models


class PhaseGroupRepository(BaseRepository[models.PhaseGroup, None, None]):
    model = models.PhaseGroup

    async def get_all_stmt(self):
        return sa.select(self.model).options(selectinload(self.model.phases)).order_by(self.model.sort_order.asc())
