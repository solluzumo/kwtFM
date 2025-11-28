from datetime import datetime

from app.models.DBModelBase import DBModelBase
from sqlalchemy import Boolean, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(DBModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    login: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    hash: Mapped[str] = mapped_column(String, nullable=False)

    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)
