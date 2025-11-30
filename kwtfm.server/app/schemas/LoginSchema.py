from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


class LoginSchema(BaseSchema):

    login: str = Field(min_length=1, max_length=32)

    password: str = Field(min_length=1, max_length=32)
