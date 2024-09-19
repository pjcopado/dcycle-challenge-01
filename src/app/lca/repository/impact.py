from src.app.common.repository import BaseRepository
from src.app.lca import models, schemas as sch


class ImpactRepository(BaseRepository[models.Impact, sch.ImpactCreateSch, sch.ImpactUpdateSch]):
    model = models.Impact
