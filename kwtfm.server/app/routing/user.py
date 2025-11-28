import bcrypt
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import func
from app.depends import get_session
from app.models.users import UserModel
from app.routing.base import EntityBaseRouter
from app.schemas.BatchUpdateResponseSchema import BatchUpdateResponseSchema
from app.schemas.ListResponseSchema import ListResponseSchema
from app.schemas.UserSchema import UserSchema
from app.schemas.FullUserSchema import FullUserSchema
from app.services.database import DBService
from datetime import datetime

class UserRouter(EntityBaseRouter):
    def __init__(
        self,
    ):
        super().__init__(
            UserModel,
            DBService,
            FullUserSchema,
        )

        self.add_routes()

    def add_routes(self):

        self.router.get(
            "/{id}",
            response_model=UserSchema,
            description="Получение информации о пользователе.",
            )(self.read)

        self.router.post(
            "s/table",
            response_model=ListResponseSchema[UserSchema],
            description="Получение списка пользователей.",
            )(self.batch_read)

        self.router.post(
            "", 
            response_model=UserSchema,
            description="Создание пользователя.",
            )(self.create)

        self.router.put(
            "/{id}", 
            response_model=UserSchema,
            description="Обновление информации о пользователе.",
            )(self.update)

        self.router.put(
            "s", 
            response_model=BatchUpdateResponseSchema[UserSchema],
            description="Обновление списка пользователей.",
            )(self.batch_update)

    async def create(self, user: FullUserSchema, session: AsyncSession = Depends(get_session)):

        service = self.service(UserModel, session, UserSchema)

        userDict = user.model_dump()

        # Проверяем, что пароль передан
        if not userDict["password"]:
            raise HTTPException(status_code=400, detail="Password is required")

        # Проверяем, что пароль не пустой
        if len(userDict["password"]) < 5:
            raise HTTPException(status_code=400, detail="Password is too short")

        # Проверяем, что пользователь с таким email не существует
        userExists = await service.getOneBy("login", userDict["login"])
        if userExists:
            raise HTTPException(status_code=400, detail="Login занят")

        # Хешируем пароль
        hashed_password = bcrypt.hashpw(userDict["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        del userDict["password"]

        userDict["created_at"] = func.now()
        userDict["hash"] = hashed_password

        users = await service.batch_insert([userDict])

        # Преобразуем модель в схему
        result = self.schema.model_validate(users[0])

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    async def update(self, id: int, user: FullUserSchema, session: AsyncSession = Depends(get_session)):

        service = self.service(UserModel, session, UserSchema)

        userDict = user.model_dump()

        if not userDict["login"] or not id or not userDict["active"]:

            raise HTTPException(status_code=400, detail="All those fields: Id, Login, Active is required")

        # Проверяем, что пароль передан
        if userDict["password"]:

            # Проверяем, что пароль не пустой
            if len(userDict["password"]) < 5:
                raise HTTPException(status_code=400, detail="Password is too short")

            # Хешируем пароль
            hashed_password = bcrypt.hashpw(userDict["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            del userDict["password"]

            userDict["hash"] = hashed_password

        # Проверяем, что пользователь с таким email не существует
        itemExists = await service.getOneBy("login", userDict["login"])

        # Если пользователь с таким email существует и это не текущий пользователь
        if itemExists and itemExists.id != id:

            raise HTTPException(status_code=400, detail="Login занят")

        model = await service.batch_update([userDict])

        if not model:

            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Item {id} were not updated",
                    "missed": {"id": id},
                },
            )

        result = self.schema.model_validate(model)  # Преобразуем модель в схему

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    async def batch_update(
        self, data: List[FullUserSchema], session: AsyncSession = Depends(get_session)
    ) -> JSONResponse:

        service = self.service(UserModel, session, UserSchema)

        # data to update
        to_update = []

        missed = []
        not_unique = []
        incorrect = []

        for item in data:

            if item.password:
                # delete password
                del item.password

            if not item.id:
                incorrect.append(item)
                continue

            if not item.login:
                incorrect.append(item)
                continue

            itemExists = await service.getOneBy("id", item.id)

            if not itemExists:
                missed.append(item.id)

            # Проверяем, что пользователь с таким email не существует
            itemExists = await service.getOneBy("login", item.login)
            if itemExists and itemExists.id != item.id:
                not_unique.append(item.id)

            # Проверяем, что запись с таким текстом не существует в других записях
            for el in data:
                if el.id != item.id and el.login == item.login:
                    not_unique.append(item.id)

            if item.id not in missed and item.id not in not_unique:
                to_update.append(item.model_dump())

        service = self.service(UserModel, session, UserSchema)
        items = await service.batch_update(to_update)

        result = [self.schema.model_validate(item) for item in items]

        content = {"list": jsonable_encoder(result)}
        status_code = 200
        if len(result) != len(data):
            status_code = 207  # 207 Multi-Status
            content["message"] = "Some items were not updated"
            content["errors"] = {}
            if not_unique:
                content["errors"]["not_unique"] = not_unique
            if missed:
                content["errors"]["missed"] = missed
            if incorrect:
                content["errors"]["incorrect"] = incorrect

        return JSONResponse(BatchUpdateResponseSchema.model_validate(content), status_code)


user_router = UserRouter().router
