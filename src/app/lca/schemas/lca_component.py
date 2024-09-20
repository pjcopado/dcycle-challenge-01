__all__ = [
    "LCAComponentCreateSch",
    "LCAComponentChildCreateSch",
    "LCAComponentUpdateSch",
    "LCAComponentSch",
    "LCAComponentHierarchySch",
]

import uuid

import pydantic

from src.app.common.schemas import OrmBaseModel, UUIDModelMixin
from src.app.lca import enum


class LCAComponentBaseSch(OrmBaseModel):
    name: str = pydantic.Field(..., min_length=2, max_length=128)
    quantity: float = pydantic.Field(...)


class LCAComponentChildCreateSch(LCAComponentBaseSch):
    source_id: uuid.UUID = pydantic.Field(...)
    components: list["LCAComponentChildCreateSch"]


class LCAComponentCreateSch(LCAComponentBaseSch):
    unit: enum.UnitEnum = pydantic.Field(...)
    phase_id: int = pydantic.Field(...)
    parent_id: uuid.UUID | None = pydantic.Field(...)
    source_id: uuid.UUID = pydantic.Field(...)
    components: list[LCAComponentChildCreateSch]


class LCAComponentUpdateSch(OrmBaseModel):
    name: str = pydantic.Field(None, min_length=2, max_length=128)
    quantity: float = pydantic.Field(None)


class LCAComponentSch(LCAComponentBaseSch, UUIDModelMixin):
    phase_id: int = pydantic.Field(...)


class LCAComponentHierarchySch(LCAComponentBaseSch, UUIDModelMixin):
    phase_id: int = pydantic.Field(...)
    components: list["LCAComponentHierarchySch"] = []
