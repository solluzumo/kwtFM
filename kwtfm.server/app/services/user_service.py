from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Type, Any, TypeVar, Generic
from app.schemas.BaseSchema import BaseSchema
from app.schemas.SortItemSchema import SortItemSchema
from app.schemas.FilterItemSchema import FilterItemSchema
from app.utils.listOperators import apply_filters, apply_sorting
from app.models.users import UserModel
from app.schemas.FullUserSchema import FullUserSchema
from app.schemas.UserSchema import UserSchema
from app.services.database import DBService
from fastapi import Depends, HTTPException
import bcrypt
T = TypeVar("T", bound=BaseSchema)


class UserService():
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.db = DBService(UserModel,session,FullUserSchema)

    async def create_user(self, user: FullUserSchema) -> UserSchema:
        data = user.model_dump()

        if not data["password"] or len(data["password"]) < 5:
            raise HTTPException(400, "Password is too short")

        if await self.db.getOneBy("login", data["login"]):
            raise HTTPException(400, "Login занят")

        hash = bcrypt.hashpw(
            data["password"].encode(), bcrypt.gensalt()
        ).decode()

        data["hash"] = hash
        data["created_at"] = func.now()
        data["updated_at"] = func.now()
        del data["password"]

        model = (await self.db.batch_insert([data]))[0]
        
        return UserSchema.model_validate(model)
        