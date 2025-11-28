from app.schemas.BaseSchema import BaseSchema
from app.utils.enums.filterLogicalOperator import FilterLogicalOperator
from app.utils.enums.filterOperator import FilterOperatorEnum
from pydantic import Field, ConfigDict
from datetime import datetime
from typing import List, Union, Optional


class FilterItemSchema(BaseSchema):
    model_config = ConfigDict(extra='ignore')

    logical: Optional[FilterLogicalOperator] = Field(FilterLogicalOperator.AND, title="Оператор")

    field: str = Field(..., title="Имя столбца")

    operator: FilterOperatorEnum = Field(..., title="Оператор сравнения")

    value: Union[int, float, str, List[str], bool, datetime] | None = Field(None, title="Значение для сравнения")
