"""Define data name of item file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'ItemItem',
        )


class ItemItem(Enum):
    NAME = 'name'
    CATEGORY = 'category'
    INFO = 'info'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DETAIL = 'detail'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value


class ItemDetail(Enum):
    APPEARANCE = 'appearance'
    SIZE = 'size'
    NOTE = 'note'
