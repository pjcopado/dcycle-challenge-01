__all__ = ["LCAImpactSch"]

from src.app.common.schemas import OrmBaseModel
from src.app.lca import enum
from .impact import *
from .phase import *
from .lca_component import *


class PhaseImpactSch(OrmBaseModel):
    code: str
    name: str
    quantity: float | None
    unit: enum.UnitEnum | None
    impact: float
    impact_distribution: float


class LCAImpactSch(OrmBaseModel):
    name: str
    phases: list[PhaseImpactSch]
