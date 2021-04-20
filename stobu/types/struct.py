"""Define struct data and record."""

# Official Libraries
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.action import ActType


__all__ = (
        'StructType',
        'StructRecord',
        'StructsData',
        )


# Main
class StructType(Enum):
    NONE = auto()
    ACTION = auto()
    COMMENT = auto()
    SCENE_DATA = auto()
    SCENE_END = auto()
    SCENE_TRANSITION = auto()
    ITEM_DATA = auto()
    TEXT = auto()
    TITLE_BOOK = auto()
    TITLE_CHAPTER = auto()
    TITLE_EPISODE = auto()
    TITLE_SCENE = auto()
    TITLE_TEXT = auto()
    FLAG_FORESHADOW = auto()
    FLAG_PAYOFF = auto()


@dataclass
class StructRecord(object):
    type: StructType
    act: ActType
    subject: str
    outline: str
    note: Any


class StructsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, StructRecord)
