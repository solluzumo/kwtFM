from datetime import datetime

from app.models.DBModelBase import DBModelBase
from sqlalchemy import Boolean, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(DBModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    login: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    hash: Mapped[str] = mapped_column(String, nullable=False)

    active:Mapped[bool] = mapped_column(Boolean, nullable=False)

    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    info: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(String(255), nullable=True)
    
    updated_at: Mapped[datetime] = mapped_column(String(255), nullable=True)