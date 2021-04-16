"""Define data name of order file."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'OrderItem',
        )


class OrderItem(Enum):
    BOOK = 'book'
    CHAPTER = 'chapter/'
    EPISODE = 'episode/'
    SCENE = 'scene/'

    def __str__(self) -> str:
        return self.value
