"""Define data name of scene file."""

# Official Librariees
from enum import Enum


__all__ = (
        'SceneItem',
        )


class SceneItem(Enum):
    TITLE = 'title'
    OUTLINE = 'outline'
    PLOT = 'plot'
    CAMERA = 'camera'
    STAGE = 'stage'
    YEAR = 'year'
    DATE = 'date'
    TIME = 'time'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
