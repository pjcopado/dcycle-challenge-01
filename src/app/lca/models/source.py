import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, UUIDMixIn


class Source(Base, UUIDMixIn):
    __tablename__ = "source"
    __mapper_args__ = {"eager_defaults": True}

    source_name: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)
    source_type: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)
    db_version: Mapped[str] = mapped_column(sa.DECIMAL(5, 2), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.source_name}, type={self.source_type})"
