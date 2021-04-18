"""Define data name of episode file."""

# Official Librariees
from enum import Enum


__all__ = (
        'EpisodeItem',
        )


class EpisodeItem(Enum):
    TITLE = 'title'
    OUTLINE = 'outline'
    PLOT = 'plot'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
