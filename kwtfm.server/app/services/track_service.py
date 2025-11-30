from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Type, Any, TypeVar, Generic

from app.schemas.BaseSchema import BaseSchema
from app.schemas.SortItemSchema import SortItemSchema
from app.schemas.FilterItemSchema import FilterItemSchema
from app.utils.listOperators import apply_filters, apply_sorting
from app.models.track import TrackModel
from app.schemas.FullTrackSchema import FullTrackSchema
from app.schemas.TrackSchema import TrackSchema
from app.services.database import DBService
from fastapi import Depends, HTTPException
import bcrypt
T = TypeVar("T", bound=BaseSchema)


class TrackService():
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.db = DBService(TrackModel,session,FullTrackSchema)

    async def create_track(self, track: FullTrackSchema) -> TrackSchema:

        data = track.model_dump()

        model = (await self.db.batch_insert([data]))[0]
        
        return TrackSchema.model_validate(model)
        