__all__ = ["PhaseSch", "PhaseGroupSch"]

import pydantic

from src.app.common.schemas import OrmBaseModel, IntegerIDModelMixin


class PhaseSch(IntegerIDModelMixin):
    code: str = pydantic.Field(..., min_length=2, max_length=8)
    name: str = pydantic.Field(..., min_length=2, max_length=64)


class PhaseGroupSch(IntegerIDModelMixin):
    sort_order: int = pydantic.Field(..., ge=0)
    name: str = pydantic.Field(..., min_length=2, max_length=64)
    phases: list[PhaseSch]
