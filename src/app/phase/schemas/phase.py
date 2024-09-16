import pydantic

from src.app.common.schemas import OrmBaseModel, IntegerIDModelMixin


class Phase(OrmBaseModel, IntegerIDModelMixin):
    code: str = pydantic.Field(..., min_length=2, max_length=8)
    name: str = pydantic.Field(..., min_length=2, max_length=64)


class PhaseGroup(OrmBaseModel):
    name: str = pydantic.Field(..., min_length=2, max_length=64)
    phases: list[Phase]
