__all__ = ["Base", "UUIDMixIn", "IntegerIDMixIn", "StringIDMixIn", "StringTagMixIn", "DeletedMixIn"]


import uuid
import datetime as dt

import sqlalchemy as sqla
from sqlalchemy.orm import DeclarativeBase, Mapped as Mapped, mapped_column as mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy.dialects.postgresql import UUID


class DBTable(DeclarativeBase):
    __table_args__ = {"extend_existing": True}
    metadata: sqla.MetaData = sqla.MetaData()

    created_at: Mapped[dt.datetime] = mapped_column(
        sqla.DateTime(timezone=True), index=True, nullable=False, server_default=sqlalchemy_functions.now(), sort_order=70
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sqla.DateTime(timezone=True), nullable=True, onupdate=sqlalchemy_functions.now(), sort_order=80
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(created_at={self.created_at!r})"


Base = DBTable


class UUIDMixIn(object):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sqla.text("gen_random_uuid()"), sort_order=-1
    )


class IntegerIDMixIn(object):
    id: Mapped[int] = mapped_column(sqla.BigInteger, primary_key=True, nullable=False, autoincrement=True, sort_order=-1)
