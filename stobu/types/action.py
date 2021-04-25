"""Define action data and record."""

# Official Libraries
from dataclasses import dataclass, field
from enum import auto, Enum


# My Modules
from stobu.types.basedata import _BaseData


__all__ = (
        'ActType',
        'ActDataType',
        'ActionRecord',
        'ActionsData',
        )


# Main
class ActType(Enum):
    NONE = 'none'
    # basic act
    DO = 'do'
    # stage drawing
    DRAW = 'draw'
    PUT = 'put'
    RID = 'rid'
    # person exists
    BE = 'be'
    COME = 'come'
    GO = 'go'
    # item owns
    HAVE = 'have'
    DISCARD = 'discard'
    # info
    EXPLAIN = 'explain'
    KNOW = 'know'
    KNOWN = 'known'
    REMEMBER = 'remember'
    # event
    OCCUR = 'occur'
    # dialogue like
    TALK = 'talk'
    THINK = 'think'
    VOICE = 'voice'
    # skin
    WEAR = 'wear'
    # status
    FEEL = 'feel'
    # control
    DATA = 'data'
    SAME = 'same'


NORMAL_ACTIONS = [
        ActType.BE,
        ActType.COME,
        ActType.DISCARD,
        ActType.DO,
        ActType.DRAW,
        ActType.EXPLAIN,
        ActType.FEEL,
        ActType.GO,
        ActType.KNOW,
        ActType.KNOWN,
        ActType.HAVE,
        ActType.OCCUR,
        ActType.PUT,
        ActType.REMEMBER,
        ActType.RID,
        ActType.TALK,
        ActType.THINK,
        ActType.VOICE,
        ActType.WEAR,
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
    FORESHADOW = auto()
    PAYOFF = auto()


TITLE_ACTIONS = [
        ActDataType.BOOK_TITLE,
        ActDataType.CHAPTER_TITLE,
        ActDataType.EPISODE_TITLE,
        ActDataType.SCENE_TITLE,
        ActDataType.SCENE_HEAD,
        ]


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
