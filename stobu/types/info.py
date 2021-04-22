"""Define scene info record and data."""

# Official Libraries
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.action import ActType


__all__ = (
        'InfoType',
        'InfoRecord',
        'InfosData',
        'SceneInfo',
        'FlagType',
        'FlagInfo',
        'StoryInfo',
        'StoryInfoType',
        )


# Main
class InfoType(Enum):
    NONE = auto()
    ACTION = auto()
    COMMENT = auto()
    SCENE_HEAD = auto()
    SCENE_END = auto()
    SCENE_TRANSITION = auto()
    TITLE_BOOK = auto()
    TITLE_CHAPTER = auto()
    TITLE_EPISODE = auto()
    TITLE_SCENE = auto()
    TITLE_TEXT = auto()
    FLAG_FORESHADOW = auto()
    FLAG_PAYOFF = auto()
    FLAG_INFO = auto()
    SPLITTER = auto()
    DATA_TITLE = auto()


INFO_TITLES = [
        InfoType.TITLE_BOOK,
        InfoType.TITLE_CHAPTER,
        InfoType.TITLE_EPISODE,
        InfoType.TITLE_SCENE,
        InfoType.TITLE_TEXT,
        ]


@dataclass
class SceneInfo(object):
    camera: str = None
    stage: str = None
    year: str = None
    date: str = None
    time: str = None
    note: str = None

    def reset(self):
        self.camera = None
        self.stage = None
        self.year = None
        self.date = None
        self.time = None
        self.note = None

    def cloned(self):
        return SceneInfo(
                self.camera, self.stage, self.year, self.date, self.time,
                self.note)


class FlagType(Enum):
    NONE = auto()
    FLAG = auto()
    DEFLAG = auto()


@dataclass
class FlagInfo(object):
    type: FlagType
    index: int
    subject: str = None
    flag: str = None
    note: str = None


class StoryInfoType(object):
    NONE = auto()
    BACKGROUND = auto()
    CHARACTER = auto()
    EVENT = auto()
    INFO = auto()
    ITEM = auto()
    SKIN = auto()


@dataclass
class StoryInfo(object):
    type: StoryInfoType
    act: ActType
    subject: str
    outline: str
    note: str


@dataclass
class InfoRecord(object):
    type: InfoType
    act: ActType
    subject: str
    outline: str
    note: Any


class InfosData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, InfoRecord)
