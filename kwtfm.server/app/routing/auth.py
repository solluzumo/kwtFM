from app.depends import get_session
from app.schemas.JWTRefreshSchema import JWTRefreshSchema
from app.schemas.LoginSchema import LoginSchema
from app.schemas.UserSchema import UserSchema
from app.schemas.ErrorMessageSchema import ErrorMessageSchema
from app.schemas.JWTBearerSchema import JWTBearerSchema
from app.services.auth import AuthService
from app.utils.auth import JWTBearer
from app.utils.log import LoggingRoute
from app.utils.token import check_token, generate_token, delete_token
from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession


class AuthRouter:
    def __init__(self):
        self.router = APIRouter(route_class=LoggingRoute)

        self.router.get(
            "/me",
            status_code=200,
            response_model=UserSchema,
            responses={403: {"description": "Forbidden"}},
            description="Получение информации о пользователе.",
        )(self.get_me)

        self.router.post(
            "/login",
            status_code=200,
            response_model=JWTBearerSchema,
            responses={404: {"description": "User not found", "model": ErrorMessageSchema}},
            description="Авторизация пользователя и получение JWT токена.",
        )(self.login)

        self.router.post(
            "/refresh",
            status_code=200,
            response_model=JWTBearerSchema,
            responses={400: {"description": "Token invalid", "model": ErrorMessageSchema}},
            description="Обновление токена доступа по refresh-токену.",
        )(self.refresh_session)

        self.router.post(
            "/log-out",
            status_code=200,
            response_model=None,
            description="Завершение сессии пользователя.",
        )(self.log_out)

    async def get_me(self, user: UserSchema = Depends(JWTBearer())) -> JSONResponse:
        return JSONResponse(jsonable_encoder(user))

    async def login(self, data: LoginSchema, session: AsyncSession = Depends(get_session)) -> JSONResponse:
        jwt = await AuthService(session).login(data)

        return JSONResponse(jsonable_encoder(jwt))

    async def refresh_session(self, data: JWTRefreshSchema) -> JSONResponse:
        login = await check_token(data.refresh_token, refresh=True)

        if login is None:
            return JSONResponse({"message": "Token invalid"}, 400)

        user = await self.service.getOneBy(field="login", value=data.login)

        return JSONResponse(
            jsonable_encoder(
                JWTBearerSchema(
                    **{
                        "access-token": await generate_token(login, user.is_admin),
                        "refresh-token": await generate_token(login, user.is_admin, True),
                    }
                )
            )
        )

    async def log_out(self, data: JWTRefreshSchema) -> Response:

        result = await delete_token(data.refresh_token)

        if not result:
            return JSONResponse({"message": "Token invalid"}, 400)

        return Response(status_code=200)


auth_router = AuthRouter().router
