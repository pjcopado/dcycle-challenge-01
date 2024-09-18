import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, UUIDMixIn


class LcaComponent(Base, UUIDMixIn):
    __tablename__ = "lca_component"
    __mapper_args__ = {"eager_defaults": True}

    lca_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("lca.id"), nullable=False)
    phase_id = Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("phase.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_id = Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("lca_component.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(sa.String(128), index=True, nullable=False)
    quantity: Mapped[float] = mapped_column(sa.DECIMAL(10, 6), nullable=False)
    unit: Mapped[str] = mapped_column(sa.String(16), index=True, nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("source.id", ondelete="CASCADE"), index=True, nullable=False)
