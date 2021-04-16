"""Define enum type for cui command."""

# Official Libraries
from enum import auto, Enum


__all__ = (
        'CmdType',
        )


class CmdType(Enum):
    NONE = auto()
    ADD = auto()
    BUILD = auto()
    COPY = auto()
    DELETE = auto()
    EDIT = auto()
    INIT = auto()
    LIST = auto()
    PUSH = auto()
    REJECT = auto()
    RENAME = auto()
    SET = auto()
