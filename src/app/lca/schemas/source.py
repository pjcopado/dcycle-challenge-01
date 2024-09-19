__all__ = ["SourceCreateSch", "SourceUpdateSch", "SourceSch"]

import pydantic

from src.app.common.schemas import OrmBaseModel, UUIDModelMixin
from .impact import ImpactSch


class SourceBaseSch(OrmBaseModel):
    source_name: str = pydantic.Field(..., min_length=2, max_length=64)
    source_type: str = pydantic.Field(..., min_length=2, max_length=64)
    db_version: float = pydantic.Field(..., ge=0)


class SourceCreateSch(SourceBaseSch):
    pass


class SourceUpdateSch(OrmBaseModel):
    source_name: str = pydantic.Field(None, min_length=2, max_length=64)
    source_type: str = pydantic.Field(None, min_length=2, max_length=64)
    db_version: float = pydantic.Field(None, ge=0)


class SourceSch(SourceBaseSch, UUIDModelMixin):
    impacts: list[ImpactSch] = None
