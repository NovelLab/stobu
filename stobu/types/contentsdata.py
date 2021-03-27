"""Define contents data and record."""

# Official Libraries
from dataclasses import dataclass, field
from enum import Enum, auto


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        'ContentRecord',
        'ContentType',
        'ContentsData',
        )


# Main
class ContentType(Enum):
    NONE = auto()
    BOOK = auto()
    CHAPTER = auto()
    EPISODE = auto()
    SCENE = auto()


@dataclass
class ContentRecord(object):
    type: ContentType
    title: str
    index: int


class ContentsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, ContentRecord)
