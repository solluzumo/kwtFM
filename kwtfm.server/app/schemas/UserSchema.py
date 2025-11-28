from app.schemas.WithIDSchema import WithIDSchema


from pydantic import Field


class UserSchema(WithIDSchema):

    login: str | None = Field(None)

    active: bool | None = Field(True)

    class Config:

        from_attributes = True
