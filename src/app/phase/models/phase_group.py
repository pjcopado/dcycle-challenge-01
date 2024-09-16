import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, IntegerIDMixIn


class PhaseGroup(Base, IntegerIDMixIn):
    __tablename__ = "phase_group"
    __mapper_args__ = {"eager_defaults": True}

    sort_order: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default="0")
    name: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"PhaseGroup({self.name})"
