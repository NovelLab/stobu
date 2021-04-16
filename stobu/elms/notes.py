"""Define data name of note file."""

# Official Librariees
from enum import Enum


__all__ = (
        'NoteItem',
        )


class NoteItem(Enum):
    NAME = 'name'
    CATEGORY = 'category'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
