"""Define data name of chapter file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'ChapterItem',
        )


class ChapterItem(Enum):
    TITLE = 'title'
    OUTLINE = 'outline'
    PLOT = 'plot'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
