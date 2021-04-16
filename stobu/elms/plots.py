"""Define data name of plot."""

# Official Librariees
from enum import auto, Enum


__all__ = (
        'PlotItem',
        )


class PlotItem(Enum):
    SETUP = 'setup'
    TP1ST = 'tp1st'
    DEVELOP = 'develop'
    TP2ND = 'tp2nd'
    CLIMAX = 'climax'
    RESOLVE = 'resolve'

    def __str__(self) -> str:
        return self.value
