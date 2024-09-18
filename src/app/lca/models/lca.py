import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, UUIDMixIn


class Lca(Base, UUIDMixIn):
    __tablename__ = "lca"
    __mapper_args__ = {"eager_defaults": True}

    name: Mapped[str] = mapped_column(sa.String(64), index=True, nullable=False)
