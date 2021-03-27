"""Define types for story record."""


# Official Libraries
from dataclasses import dataclass, field
from enum import Enum, auto


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        'StoryRecord',
        'StoryRecordType',
        'StoryData',
        )


# Main
class StoryRecordType(Enum):
    NONE = auto()
    BOOK = auto()
    CHAPTER = auto()
    EPISODE = auto()
    SCENE = auto()


@dataclass
class StoryRecord(object):
    type: StoryRecordType
    filename: str
    data: dict = field(default_factory=dict)


class StoryData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, StoryRecord)
