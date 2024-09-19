import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, IntegerIDMixIn


class Phase(Base, IntegerIDMixIn):
    __tablename__ = "phase"
    __mapper_args__ = {"eager_defaults": True}

    group_id: Mapped[int] = mapped_column(sa.ForeignKey("phase_group.id", ondelete="CASCADE"), index=True, nullable=False)
    code: Mapped[str] = mapped_column(sa.String(8), index=True, nullable=False)
    name: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code}, name={self.name})"
