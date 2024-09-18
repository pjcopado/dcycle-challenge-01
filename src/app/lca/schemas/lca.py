__all__ = ["LCACreateSch", "LCASch"]

import pydantic

from src.app.common.schemas import OrmBaseModel, UUIDModelMixin
from .lca_component import LCAComponentSch


class LCABaseSch(OrmBaseModel):
    name: str = pydantic.Field(..., min_length=2, max_length=64)


class LCACreateSch(LCABaseSch):
    pass


class LCASch(LCABaseSch, UUIDModelMixin):
    components: list[LCAComponentSch]
