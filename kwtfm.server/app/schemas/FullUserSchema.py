from app.schemas.WithIDSchema import WithIDSchema

from pydantic import Field


class FullUserSchema(WithIDSchema):

    login: str | None = Field(None)

    password: str | None = Field(None)

    active: bool | None = Field(True)

    is_admin: bool | None = Field(True)

    class Config:
        from_attributes = True
