"""Define data name of rubi."""

# Official Librariees
from enum import Enum


__all__ = (
        'RubiItem',
        )


class RubiItem(Enum):
    RUBI = 'rubi'
    EXCLUSIONS = 'exclusions'
    ALWAYS = 'always'

    def __str__(self) -> str:
        return self.value
