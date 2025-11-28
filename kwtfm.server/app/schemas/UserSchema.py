from app.schemas.WithIDSchema import WithIDSchema


from pydantic import Field


class UserSchema(WithIDSchema):

    login: str

    active: bool

    info: str

    class Config:

        from_attributes = True
