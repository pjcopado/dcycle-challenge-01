import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, UUIDMixIn


class Impact(Base, UUIDMixIn):
    __tablename__ = "impact"
    __mapper_args__ = {"eager_defaults": True}

    value: Mapped[float] = mapped_column(sa.Column(sa.DECIMAL(10, 6), nullable=False))
    category: Mapped[str] = mapped_column(sa.Column(sa.String(64), nullable=False))
    source_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("source.id", ondelete="CASCADE"), index=True, nullable=False)
