import bcrypt
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import func
from app.depends import get_session
from app.models.track import TrackModel
from app.routing.base import EntityBaseRouter
from app.schemas.BatchUpdateResponseSchema import BatchUpdateResponseSchema
from app.schemas.ListResponseSchema import ListResponseSchema
from app.schemas.TrackSchema import TrackSchema
from app.schemas.FullTrackSchema import FullTrackSchema
from app.schemas.UserSchema import UserSchema
from app.services.track_service import TrackService
from datetime import datetime
from app.utils.auth import JWTBearer

class TrackRouter(EntityBaseRouter):
    def __init__(
        self,
    ):
        super().__init__(
            TrackModel,
            TrackService,
            FullTrackSchema,
        )

        self.add_routes()

    def add_routes(self):

        self.router.get(
            "/{id}",
            response_model=FullTrackSchema,
            description="Получение подробной информации о треке.",
            )(self.read)

        self.router.post(
            "s/table",
            response_model=ListResponseSchema[TrackSchema],
            description="Получение списка треков.",
            )(self.batch_read)

        self.router.post(
            "", 
            response_model=TrackSchema,
            description="Создание трека.",
            )(self.create)

        self.router.put(
            "/{id}", 
            response_model=TrackSchema,
            description="Обновление информации о треке.",
            )(self.update)

        self.router.put(
            "s", 
            response_model=BatchUpdateResponseSchema[TrackSchema],
            description="Обновление списка треков.",
            )(self.batch_update)
        
    async def create(self, 
                     track: FullTrackSchema, 
                     session: AsyncSession = Depends(get_session),
                     user: UserSchema = Depends(JWTBearer())):
        
        service = TrackService(session=session)

        result = await service.create_track(track)

        return result
    
    
    async def like(self, 
                     track: TrackSchema, 
                     session: AsyncSession = Depends(get_session),
                     user:UserSchema = Depends(JWTBearer())):

        service = TrackService(session=session)

        result = await service.like_track(track)

        return result
    

track_router = TrackRouter().router