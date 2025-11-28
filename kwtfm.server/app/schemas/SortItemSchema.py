from app.schemas.BaseSchema import BaseSchema
from app.utils.enums.sortDirection import SortDirectionEnum


from pydantic import Field


class SortItemSchema(BaseSchema):

    field: str = Field(..., title="Имя столбца")

    sort: SortDirectionEnum = Field(..., title="Направление сортировки")
