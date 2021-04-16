"""Define data name of book file."""

# Official Librariees
from enum import Enum


__all__ = (
        'BookItem',
        )


class BookItem(Enum):
    TITLE = 'title'
    COPY = 'copy'
    THEME = 'theme'
    GENRE = 'genre'
    TARGET = 'target'
    SIZE = 'size'
    COLUMNS = 'columns'
    ROWS = 'rows'
    CONTEST = 'contest'
    CAUTION = 'caution'
    SITES = 'sites'
    TAGS = 'tags'
    VERSION = 'version'
    RELEASED = 'released'
    OUTLINE = 'outline'
    PLOT = 'plot'
    NOTE = 'note'

    def __str__(self) -> str:
        return self.value
