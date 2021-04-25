"""Define element types."""

# Official Libraries
from enum import Enum


# My Modules


__all__ = (
        'ElmType',
        'BASE_FILES',
        )


class ElmType(Enum):
    NONE = 'none'
    # basic
    BOOK = 'book'
    ORDER = 'order'
    PROJECT = 'project'
    # story
    CHAPTER = 'chapter'
    EPISODE = 'episode'
    SCENE = 'scene'
    NOTE = 'note'
    OUTLINE = 'outline'
    PLAN = 'plan'
    # item
    PERSON = 'person'
    STAGE = 'stage'
    ITEM = 'item'
    WORD = 'word'
    EVENT = 'event'
    # utility
    BUILD = 'build'
    FIXTURE = 'fixture'
    MATERIAL = 'material'
    MOB = 'mob'
    RUBI = 'rubi'
    TERM = 'term'
    TIME = 'time'
    TODO = 'todo'
    TRASH = 'trash'
    # data
    PLOT = 'plot'

    def __str__(self):
        return self.value


BASE_FILES = [
        ElmType.BOOK,
        ElmType.FIXTURE,
        ElmType.MOB,
        ElmType.ORDER,
        ElmType.RUBI,
        ElmType.TERM,
        ElmType.TIME,
        ElmType.TODO,
        ]
