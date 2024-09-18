__all__ = ["LCASch", "LCAComponentSch"]

import uuid

import pydantic

from src.app.common.schemas import OrmBaseModel, UUIDModelMixin
from src.app.lca import enum


class LCAComponentBaseSch(OrmBaseModel):
    name: str = pydantic.Field(..., min_length=2, max_length=128)
    quantity: float = pydantic.Field(...)
    unit: enum.UnitEnum = pydantic.Field(...)


class LCAComponentCreateSch(LCAComponentBaseSch):
    lca_id: uuid.UUID = pydantic.Field(...)
    phase_id: uuid.UUID = pydantic.Field(...)
    parent_id: uuid.UUID | None = pydantic.Field(...)
    source_id: uuid.UUID = pydantic.Field(...)


class LCAComponentSch(LCAComponentBaseSch, UUIDModelMixin):
    pass
