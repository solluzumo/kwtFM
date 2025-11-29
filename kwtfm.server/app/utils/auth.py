from app.database import session_maker
from app.models.users import UserModel
from app.schemas.UserSchema import UserSchema
from app.services.database import DBService
from app.utils.token import check_token, check_admin
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer


class JWTBearer(HTTPBearer):
    def __init__(self, require_admin: bool = False):
        super().__init__()
        self.require_admin = require_admin
    
    async def __call__(self,request: Request) ->UserSchema:
        #Парсим и достаем тело токена из запроса
        authorization: str| None = request.headers.get("Authorization")

        #Если токена нет
        if not authorization or not authorization.startswith("Bearer"):
            raise HTTPException(status_code=403, detail="Неверный формат заголовка авторизации")
        
        token = authorization[len("Bearer "):]

        if token:
            token_data = await self._decode_jwt(token)

            return token_data
        
        raise HTTPException(status_code=500, detail="Internal server exception with JWT")
    
    async def _decode_jwt(token:str)->UserSchema:
        
        login = await check_token(token)

        if login:
            return UserSchema(login=login)

        raise HTTPException(status_code=401, detail="User deactivated or deleted")









