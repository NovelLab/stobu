"""Define data name of event file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'EventItem',
        )


class EventItem(Enum):
    NAME = 'name'
    OUTLINE = 'outline'
    STAGE = 'stage'
    YEAR = 'year'
    DATE = 'date'
    TIME = 'time'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
