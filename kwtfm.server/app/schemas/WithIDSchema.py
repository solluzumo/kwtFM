from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


class WithIDSchema(BaseSchema):

    id: int = Field(None)
