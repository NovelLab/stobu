"""Define struct data and record."""

# Official Libraries
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Any


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.action import ActType


__all__ = (
        'StructType',
        'StructRecord',
        'StructsData',
        'STRUCT_TITLES',
        'SceneDataInfo',
        )


# Main
class StructType(Enum):
    NONE = auto()
    ACTION = auto()
    COMMENT = auto()
    SCENE_END = auto()
    TEXT = auto()
    TITLE_BOOK = auto()
    TITLE_CHAPTER = auto()
    TITLE_EPISODE = auto()
    TITLE_SCENE = auto()
    TITLE_TEXT = auto()
    # DATA
    SCENE_DATA = auto()
    PERSON_DATA = auto()
    ITEM_DATA = auto()
    EVENT_DATA = auto()


STRUCT_TITLES = [
        StructType.TITLE_BOOK,
        StructType.TITLE_CHAPTER,
        StructType.TITLE_EPISODE,
        StructType.TITLE_SCENE,
        StructType.TITLE_TEXT,
        ]


class DataInfoType(Enum):
    NONE = auto()
    PERSON = auto()
    ITEM = auto()
    EVENT = auto()


@dataclass
class SceneDataInfo(object):
    type: DataInfoType
    data: list = field(default_factory=list)

    def append(self, val):
        self.data.append(val)

    def cloned(self):
        return SceneDataInfo(self.type, self.data)

    def reset(self):
        self.data = []


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
