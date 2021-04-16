"""Define novel data and record."""

# Official Libraries
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


# My Modules
from stobu.types.basedata import _BaseData


__all__ = (
        'NovelType',
        'NovelRecord',
        'NovelsData',
        )


# Main
class NovelType(Enum):
    NONE = auto()
    COMMENT = auto()
    DESCRIPTION = auto()
    DIALOGUE = auto()
    PLAIN = auto()
    TITLE_BOOK = auto()
    TITLE_CHAPTER = auto()
    TITLE_EPISODE = auto()
    TITLE_SCENE = auto()
    TITLE_TEXT = auto()
    BR = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()


@dataclass
class NovelRecord(object):
    type: NovelType
    subject: str
    desc: str
    note: Any


class NovelsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, NovelRecord)
