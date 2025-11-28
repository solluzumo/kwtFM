from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Any

from app.models.DBModelBase import DBModelBase
from app.depends import get_session
from app.utils.log import LoggingRoute
from app.schemas.ListRequestSchema import ListRequestSchema
from app.schemas.ListResponseSchema import ListResponseSchema
from app.schemas.BaseSchema import BaseSchema
from app.services.database import DBService

# Обобщенные типы для моделей и схем
MODEL = TypeVar("MODEL", bound=DBModelBase)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)


class EntityBaseRouter:

    def __init__(
        #
        self,
        model: type[MODEL],
        service: type[DBService],
        schema: type[SCHEMA],
    ):
        self.model = model
        self.service = service
        self.schema = schema
        self.router = APIRouter(route_class=LoggingRoute)

    async def read(self, id: int, session: AsyncSession = Depends(get_session)):

        service = self.service(self.model, session, self.schema)
        model = await service.getOneBy("id", id)

        if model is None:

            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Item {id} were not found",
                    "missed": {"id": id},
                },
            )

        result = self.schema.model_validate(jsonable_encoder(model))  # Преобразуем модель в схему

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    async def read_number(self, number: str, session: AsyncSession = Depends(get_session)):

        service = self.service(self.model, session, self.schema)
        model = await service.getOneBy("number", number)

        if model is None:

            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Item {number} were not found",
                    "missed": {"number": number},
                },
            )

        result = self.schema.model_validate(jsonable_encoder(model))  # Преобразуем модель в схему

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    async def batch_read(
        self,
        listRequest: ListRequestSchema,
        session: AsyncSession = Depends(get_session),
    ):

        service = self.service(self.model, session, self.schema)
        result = await service.select(
            listRequest.sorting, listRequest.filtering, listRequest.page, listRequest.pageSize
        )

        rows = [self.schema.model_validate(item) for item in result["rows"]]

        return ListResponseSchema[self.schema](
            rows=rows,
            totalRows=result["totalRows"],
        )
