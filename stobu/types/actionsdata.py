"""Define action data and record."""

# Official Libraries
from dataclasses import dataclass, field
from enum import Enum, auto


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        )


# Main
class ActRecordType(Enum):
    NONE = auto()
    ACTION = auto()
    BR = auto()
    COMMENT = auto()
    INDENT = auto()
    INSTRUCTION = auto()
    SCENE_DATA = auto()
    TEXT = auto()
    TITLE = auto()


@dataclass
class ActionRecord(object):
    type: ActRecordType
    subject: str
    action: str = ""
    outline: str = ""
    desc: str = ""
    flags: list = field(default_factory=list)
    note: str = ""


class ActionData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, ActionRecord)
