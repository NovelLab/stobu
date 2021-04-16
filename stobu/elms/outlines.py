"""Define data name of outline file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'OutlineItem',
        )


class OutlineItem(Enum):
    NAME = 'name'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
