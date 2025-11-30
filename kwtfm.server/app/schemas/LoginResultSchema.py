from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


class LoginResultSchema(BaseSchema):

    authorised: bool = Field(default=False, title="Authorisation status")

    message: str = Field(default="", title="Message")
