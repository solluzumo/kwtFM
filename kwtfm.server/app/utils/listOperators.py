from app.utils.enums.filterLogicalOperator import FilterLogicalOperator
from sqlalchemy.sql import Select, or_, and_
from sqlalchemy import cast, String
from datetime import datetime, timedelta
from typing import List, Type
#from sqlalchemy.dialects import postgresql

from app.schemas.SortItemSchema import SortItemSchema
from app.schemas.FilterItemSchema import FilterItemSchema
from app.utils.enums.filterOperator import FilterOperatorEnum

main_operators = {
    FilterOperatorEnum.gte: lambda field, value: field >= value,
    FilterOperatorEnum.gte_math: lambda field, value: field >= value,
    FilterOperatorEnum.lte: lambda field, value: field <= value,
    FilterOperatorEnum.lte_math: lambda field, value: field <= value,
    FilterOperatorEnum.equals: lambda field, value: field == value,
    FilterOperatorEnum.equals_math: lambda field, value: field == value,
    FilterOperatorEnum.doesNotEqual: lambda field, value: field != value,
    FilterOperatorEnum.doesNotEqual_math: lambda field, value: field != value,
    FilterOperatorEnum.lt: lambda field, value: field < value,
    FilterOperatorEnum.lt_math: lambda field, value: field < value,
    FilterOperatorEnum.gt: lambda field, value: field > value,
    FilterOperatorEnum.gt_math: lambda field, value: field > value,
    FilterOperatorEnum.contains: lambda field, value: cast(field, String).contains(value),
    FilterOperatorEnum.doesNotContain: lambda field, value: ~cast(field, String).contains(value),
    FilterOperatorEnum.startsWith: lambda field, value: cast(field, String).startswith(value),
    FilterOperatorEnum.endsWith: lambda field, value: cast(field, String).endswith(value),
}

none_operator_map = {
    FilterOperatorEnum.is_: lambda field: field.is_(None),
    FilterOperatorEnum.not_: lambda field: field.isnot(None),
    FilterOperatorEnum.isEmpty: lambda field: (field == None) | (cast(field, String) == ""),
    FilterOperatorEnum.isNotEmpty: lambda field: (field != None) & (cast(field, String) != ""),
}

bool_operator_map = {
    FilterOperatorEnum.is_: lambda field, value: field.is_(value),
}

datetime_operator_map = {
    FilterOperatorEnum.is_: lambda field, value: field == value,
    FilterOperatorEnum.not_: lambda field, value: field != value,
    FilterOperatorEnum.after: lambda field, value: field > value,
    FilterOperatorEnum.onOrAfter: lambda field, value: field >= value,
    FilterOperatorEnum.before: lambda field, value: field < value,
    FilterOperatorEnum.onOrBefore: lambda field, value: field <= value,
}

list_operator_map = {
    FilterOperatorEnum.isAnyOf: lambda field, value: cast(field, String).in_(value),
}

string_operator_map = {
    FilterOperatorEnum.is_: lambda field, value: cast(field, String) == value,
    FilterOperatorEnum.not_: lambda field, value: cast(field, String) != value,
}


def apply_filters(query: Select, filters: List[FilterItemSchema], model: Type) -> Select:
    if not filters:
        return query

    has_or_operator = any(
        filter_item.logical == FilterLogicalOperator.OR 
        for filter_item in filters 
        if hasattr(filter_item, 'logical')
    )
    
    if has_or_operator:
        # Все условия объединяем через OR
        or_conditions = []
        for filter_item in filters:
            condition = _build_condition(filter_item, model)
            if condition is not None:
                or_conditions.append(condition)
        
        if or_conditions:
            query = query.where(or_(*or_conditions))
    else:
        # Все условия объединяем через AND
        and_conditions = []
        for filter_item in filters:
            condition = _build_condition(filter_item, model)
            if condition is not None:
                and_conditions.append(condition)
        
        if and_conditions:
            query = query.where(and_(*and_conditions))
    
    #print(query.compile(dialect=postgresql.dialect()))
    
    return query

def _build_condition(filter_item: FilterItemSchema, model: Type):
    """Создает условие фильтрации для одного фильтра"""
    
    field = getattr(model, filter_item.field)
    operator = filter_item.operator
    value = filter_item.value

    if value is None:
        if operator in none_operator_map:
            return none_operator_map[operator](field)

    elif operator in main_operators:
        condition = main_operators[operator](field, value)
        if condition is not None:
            return condition

    elif operator == FilterOperatorEnum.isArrayColumnContains:
        if isinstance(value, int):
            return field.contains([value])

    elif isinstance(value, bool):
        if operator in bool_operator_map:
            return bool_operator_map[operator](field, value)

    elif isinstance(value, list):
        if operator in list_operator_map:
            return list_operator_map[operator](field, value)

    elif _is_datetime(value):
        if operator in datetime_operator_map:
            if operator in [FilterOperatorEnum.is_, FilterOperatorEnum.not_]:
                start_of_day, start_of_next_day = _get_date_range(value)
                if operator == FilterOperatorEnum.is_:
                    return (field >= start_of_day) & (field < start_of_next_day)
                elif operator == FilterOperatorEnum.not_:
                    return (field < start_of_day) | (field >= start_of_next_day)
            else:
                return datetime_operator_map[operator](field, _is_datetime(value))

    elif isinstance(value, str):
        if operator in string_operator_map:
            return string_operator_map[operator](field, value)

    else:
        print(f"{datetime.now()} unsupported filter operator: {operator}")
    
    return None


def apply_sorting(query: Select, sorting: List[SortItemSchema], model: Type) -> Select:

    for sort_item in sorting:

        field = getattr(model, sort_item.field)

        if sort_item.sort == "asc":

            query = query.order_by(field.asc().nulls_last())

        elif sort_item.sort == "desc":

            query = query.order_by(field.desc().nulls_last())

    return query


def _is_datetime(text) -> datetime | bool:

    try:

        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%fZ")

    except (ValueError, TypeError):

        return False


def _get_date_range(value: str):
    """Преобразует строку с датой в диапазон от начала дня до начала следующего дня."""

    date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)

    start_of_next_day = start_of_day + timedelta(days=1)

    return start_of_day, start_of_next_day
