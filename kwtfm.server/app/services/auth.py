import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserModel
from app.schemas.LoginResultSchema import LoginResultSchema
from app.schemas.LoginSchema import LoginSchema
from app.services.database import DBService
from app.schemas.JWTBearerSchema import JWTBearerSchema
from app.schemas.UserSchema import UserSchema
from app.utils.token import generate_token


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.service = DBService(UserModel, session, UserSchema)

    async def login(self, data: LoginSchema) -> LoginResultSchema | JWTBearerSchema:

        user = await self.service.getOneBy(field="login", value=data.login)

        if not isinstance(user, UserModel) and user is not None:
            return LoginResultSchema(
                authorised=False,
                message="Bad request",
            )

        if user is None:
            return LoginResultSchema(
                authorised=False,
                message="User not found",
            )

        if not bcrypt.checkpw(data.password.encode("utf-8"), user.hash.encode("utf-8")):
            return LoginResultSchema(
                authorised=False,
                message="Password incorrect",
            )

        return JWTBearerSchema(
            **{
                "access-token": await generate_token(login=data.login, is_admin=user.is_admin, refresh=False),
                "refresh-token": await generate_token(data.login, user.is_admin, True),
            }
        )
