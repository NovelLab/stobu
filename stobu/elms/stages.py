"""Define data name of stage file."""

# Official Librariees
from enum import Enum


__all__ = (
        'StageItem',
        )


class StageItem(Enum):
    NAME = 'name'
    CATEGORY = 'category'
    INFO = 'info'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DETAIL = 'detail'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value


class StageDetail(Enum):
    APPEARANCE = 'appearance'
    STRUCTURE = 'structure'
    NOTE = 'note'
