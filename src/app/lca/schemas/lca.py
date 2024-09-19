__all__ = ["LCACreateSch", "LCAUpdateSch", "LCASch"]

import pydantic

from src.app.common.schemas import OrmBaseModel, UUIDModelMixin


class LCABaseSch(OrmBaseModel):
    name: str = pydantic.Field(..., min_length=2, max_length=64)


class LCACreateSch(LCABaseSch):
    pass


class LCAUpdateSch(OrmBaseModel):
    name: str = pydantic.Field(None, min_length=2, max_length=64)


class LCASch(LCABaseSch, UUIDModelMixin):
    pass
