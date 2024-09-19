from src.app.common.repository import BaseRepository
from src.app.lca import models, schemas as sch


class SourceRepository(BaseRepository[models.Source, sch.SourceCreateSch, sch.SourceUpdateSch]):
    model = models.Source
