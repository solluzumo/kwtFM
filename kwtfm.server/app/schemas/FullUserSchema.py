from app.schemas.WithIDSchema import WithIDSchema

from pydantic import Field


class FullUserSchema(WithIDSchema):

    login: str

    password: str

    active: bool

    is_admin: bool

    email: str

    info: str

    class Config:
        from_attributes = True
