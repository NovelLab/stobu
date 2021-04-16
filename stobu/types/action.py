"""Define action data and record."""

# Official Libraries
from dataclasses import dataclass, field
from enum import auto, Enum


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.element import ElmType


__all__ = (
        'ActRecordType',
        'ActionRecord',
        'ActionsData',
        )


# Main
class ActType(Enum):
    NONE = 'none'
    # basic act
    BE = 'be'
    COME = 'come'
    DO = 'do'
    DRAW = 'draw'
    EXPLAIN = 'explain'
    GO = 'go'
    OCCUR = 'occur'
    TALK = 'talk'
    THINK = 'think'
    VOICE = 'voice'
    # control
    DATA = 'data'
    SAME = 'same'


NORMAL_ACTIONS = [
        ActType.BE,
        ActType.COME,
        ActType.DO,
        ActType.DRAW,
        ActType.EXPLAIN,
        ActType.GO,
        ActType.OCCUR,
        ActType.TALK,
        ActType.THINK,
        ActType.VOICE,
        ]


class ActDataType(Enum):
    NONE = auto()
    COMMENT = auto()
    TEXT = auto()
    INSTRUCTION = auto()
    BOOK_TITLE = auto()
    CHAPTER_TITLE = auto()
    EPISODE_TITLE = auto()
    SCENE_TITLE = auto()
    SCENE_START = auto()
    SCENE_END = auto()
    SCENE_CAMERA = auto()
    SCENE_STAGE = auto()
    SCENE_YEAR = auto()
    SCENE_DATE = auto()
    SCENE_TIME = auto()
    SCENE_HEAD = auto()
    BR = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()


@dataclass
class ActionRecord(object):
    type: ActType
    subtype: ActDataType
    subject: str = ""
    outline: str = ""
    desc: str = ""
    flags: list = field(default_factory=list)
    note: str = ""


class ActionsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, ActionRecord)
