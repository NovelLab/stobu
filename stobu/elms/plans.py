"""Define data name of plan file."""

# Official Librariees
from enum import Enum


__all__ = (
        'PlanItem',
        )


class PlanItem(Enum):
    NAME = 'name'
    KEYWORDS = 'keywords'
    NOTE = 'note'
    DATA = 'markdown'

    def __str__(self) -> str:
        return self.value
