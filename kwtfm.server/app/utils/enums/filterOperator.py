from enum import Enum


class FilterOperatorEnum(str, Enum):
    gte = "gte"  # greater than or equal
    lte = "lte"  # less than or equal
    equals = "equals"  # equals
    doesNotEqual = "doesNotEqual"
    lt = "lt"  # less than
    gt = "gt"  # greater than
    startsWith = "startsWith"
    endsWith = "endsWith"
    is_ = "is"
    not_ = "not"
    after = "after"
    onOrAfter = "onOrAfter"
    before = "before"
    onOrBefore = "onOrBefore"
    equals_math = "="
    doesNotEqual_math = "!="
    gt_math = ">"
    gte_math = ">="
    lt_math = "<"
    lte_math = "<="
    isEmpty = "isEmpty"
    isNotEmpty = "isNotEmpty"
    isAnyOf = "isAnyOf"
    contains = "contains"
    doesNotContain = "doesNotContain"
    isArrayColumnContains = "isArrayColumnContains"
