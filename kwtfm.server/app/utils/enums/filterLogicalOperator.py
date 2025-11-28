from enum import Enum


class FilterLogicalOperator(str, Enum):
    AND = "and"
    OR = "or"
