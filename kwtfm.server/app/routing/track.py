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
from app.schemas.TrackSchema import TackSchema
from app.schemas.FullTrackSchema import FullTrackSchema
from app.services.database import DBService
from datetime import datetime

class TrackRouter(EntityBaseRouter):
    def __init__(
        self,
    ):
        super().__init__(
            TrackModel,
            DBService,
            FullTrackSchema,
        )

        self.add_routes()

    def add_routes(self):

        self.router.get(
            "/{id}",
            response_model=FullTrackSchema,
            description="Получение информации о треке.",
            )(self.read)

        self.router.post(
            "s/table",
            response_model=ListResponseSchema[TackSchema],
            description="Получение списка треков.",
            )(self.batch_read)

        self.router.post(
            "", 
            response_model=TackSchema,
            description="Создание трека.",
            )(self.create)

        self.router.put(
            "/{id}", 
            response_model=TackSchema,
            description="Обновление информации о треке.",
            )(self.update)

        self.router.put(
            "s", 
            response_model=BatchUpdateResponseSchema[TackSchema],
            description="Обновление списка треков.",
            )(self.batch_update)
        