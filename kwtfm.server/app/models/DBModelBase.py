from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


class DBModelBase(DeclarativeBase):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
