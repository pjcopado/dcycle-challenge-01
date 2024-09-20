import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.database import Base


class LCAComponent(Base):
    __tablename__ = "lca_component"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"), sort_order=-1
    )
    lca_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("lca.id"), nullable=False)
    phase_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("phase.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("lca_component.id", ondelete="CASCADE"), index=True, nullable=True)
    name: Mapped[str] = mapped_column(sa.String(128), index=True, nullable=False)
    quantity: Mapped[float] = mapped_column(sa.DECIMAL(12, 6), nullable=False)
    unit: Mapped[str] = mapped_column(sa.String(16), index=True, nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("source.id", ondelete="CASCADE"), index=True, nullable=False)

    lca = relationship("LCA", back_populates="components")
    parent: Mapped["LCAComponent"] = relationship(remote_side=[id], back_populates="components")
    components: Mapped[list["LCAComponent"]] = relationship(
        back_populates="parent",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
