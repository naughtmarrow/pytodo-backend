from enum import Enum


class PriorityType(Enum):
    URGENT = (1,)
    IMPORTANT = (2,)
    NORMAL = (3,)
    OPTIONAL = 4
