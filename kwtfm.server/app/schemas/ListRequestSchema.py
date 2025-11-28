from app.schemas.BaseSchema import BaseSchema
from app.schemas.FilterItemSchema import FilterItemSchema
from app.schemas.SortItemSchema import SortItemSchema
from app.utils.enums.filterOperator import FilterOperatorEnum
from app.utils.enums.sortDirection import SortDirectionEnum

from typing import List
from pydantic import Field

class ListRequestSchema(BaseSchema):

    page: int = Field(0, ge=0, title="Номер страницы")

    pageSize: int = Field(10, gt=0, title="Количество элементов на странице")

    sorting: List[SortItemSchema] = Field(
        [], examples=[SortItemSchema(field="id", sort=SortDirectionEnum.desc)], title="Параметры сортировки"
    )

    filtering: List[FilterItemSchema] = Field(
        [],
        examples=[FilterItemSchema(field="id", operator=FilterOperatorEnum.after, value=5, logical = None)],
        title="Параметры фильтрации",
    )
