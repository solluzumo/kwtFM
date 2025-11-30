from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


class JWTBearerSchema(BaseSchema):

    access_token: str = Field(min_length=1, max_length=255, alias="access-token")

    refresh_token: str = Field(min_length=1, max_length=255, alias="refresh-token")
