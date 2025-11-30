from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


class JWTRefreshSchema(BaseSchema):

    refresh_token: str = Field(alias="refresh-token")
