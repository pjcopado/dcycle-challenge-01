import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.database import Base, IntegerIDMixIn
from .phase import Phase


class PhaseGroup(Base, IntegerIDMixIn):
    __tablename__ = "phase_group"
    __mapper_args__ = {"eager_defaults": True}

    sort_order: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default="0")
    name: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)

    phases: Mapped[list[Phase]] = relationship("Phase", backref="phase_group", order_by="Phase.code.asc()")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
