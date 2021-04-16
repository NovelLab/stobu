"""Define data name of time file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'TimeItem',
        )


class TimeItem(Enum):
    EARLYMORNING = 'earlymorning'
    MORNING = 'morning'
    MIDMORNING = 'midmorning'
    NOON = 'noon'
    AFTERNOON = 'afternoon'
    AFTERSCHOOL = 'afterschool'
    EVENING = 'evening'
    NIGHT = 'night'
    LATEIGHT = 'latenight'
    MIDNIGHT = 'midnight'
    DEEPNIGHT = 'deepnight'
    DAWN = 'dawn'

    def __str__(self) -> str:
        return self.value
