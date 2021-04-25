"""Define data name of time file."""

# Official Librariees
from enum import Enum


__all__ = (
        'TimeItem',
        )


class TimeItem(Enum):
    NAME = 'name'
    TIME = 'time'

    def __str__(self) -> str:
        return self.value
