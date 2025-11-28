from app.schemas.BaseSchema import BaseSchema
from app.schemas.BatchUpdateErrorsSchema import BatchUpdateErrorsSchema


from pydantic import Field


from typing import TypeVar, Generic

T = TypeVar("T", bound=BaseSchema)


class BatchUpdateResponseSchema(BaseSchema, Generic[T]):

    rows: list[T] | None = Field(..., title="Список записей")

    message: str | None = Field(..., title="Общее количество записей")

    errors: BatchUpdateErrorsSchema | None = Field(..., title="Общее количество записей")

    class Config:
        from_attributes = True
