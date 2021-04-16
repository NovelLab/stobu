"""Define element types."""

# Official Libraries
from enum import Enum, auto


# My Modules


__all__ = (
        'ElmType',
        )


class ElmType(Enum):
    NONE = 'none'
    CHAPTER = 'chapter'
    EPISODE = 'episode'
    SCENE = 'scene'
    NOTE = 'note'
    PERSON = 'person'
    STAGE = 'stage'
    ITEM = 'item'
    WORD = 'word'
    EVENT = 'event'
    MATERIAL = 'material'
    OUTLINE = 'outline'
    PLAN = 'plan'
    PROJECT = 'project'
    BOOK = 'book'
    ORDER = 'order'
    MOB = 'mob'
    RUBI = 'rubi'
    TIME = 'time'
    TODO = 'todo'
    TRASH = 'trash'
    BUILD = 'build'
    PLOT = 'plot'

    def __str__(self):
        return self.value
