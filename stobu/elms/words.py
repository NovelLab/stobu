"""Define data name of word file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'WordItem',
        )


class WordItem(Enum):
    NAME = 'name'
    CATEGORY = 'category'
    INFO = 'info'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
