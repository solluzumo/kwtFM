from app.schemas.BaseSchema import BaseSchema


from pydantic import Field


from typing import TypeVar, Generic

T = TypeVar("T", bound=BaseSchema)


class ListResponseSchema(BaseSchema, Generic[T]):

    rows: list[T] = Field(..., title="Список записей")

    totalRows: int = Field(..., title="Общее количество записей")
