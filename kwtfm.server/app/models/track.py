from datetime import datetime

from app.models.DBModelBase import DBModelBase
from sqlalchemy import Boolean, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class TrackModel(DBModelBase):
    __tablename__ = "tracks"
    



