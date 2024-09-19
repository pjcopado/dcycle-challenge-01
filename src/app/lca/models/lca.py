import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.database import Base, UUIDMixIn
from .lca_component import LCAComponent


class LCA(Base, UUIDMixIn):
    __tablename__ = "lca"
    __mapper_args__ = {"eager_defaults": True}

    name: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)

    components: Mapped[list[LCAComponent]] = relationship(
        back_populates="lca",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
