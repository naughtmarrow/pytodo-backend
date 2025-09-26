from enum import Enum

from psycopg2.extensions import QuotedString, register_adapter


class PriorityType(int, Enum):
    URGENT = 1
    IMPORTANT = 2
    NORMAL = 3
    OPTIONAL = 4


def _priority_type_adapter(pt: PriorityType):
    return QuotedString(pt.name)


register_adapter(PriorityType, _priority_type_adapter)
