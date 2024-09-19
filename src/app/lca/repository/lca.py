from src.app.common.repository import BaseRepository
from src.app.lca import models, schemas as sch


class LCARepository(BaseRepository[models.LCA, sch.LCACreateSch, sch.LCAUpdateSch]):
    model = models.LCA
