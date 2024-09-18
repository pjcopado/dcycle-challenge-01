__all__ = ["ImpactCreateSch", "ImpactSch"]

import uuid

import pydantic

from src.app.common.schemas import OrmBaseModel, UUIDModelMixin


class ImpactBaseSch(OrmBaseModel):
    value: float = pydantic.Field(...)
    category: str = pydantic.Field(..., min_length=2, max_length=64)


class ImpactCreateSch(ImpactBaseSch):
    source_id: uuid.UUID = pydantic.Field(...)


class ImpactSch(ImpactBaseSch, UUIDModelMixin):
    pass
