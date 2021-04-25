"""Define data name of state file."""

# Official Libraries
from enum import Enum


__all__ = (
        'StateItem',
        )


# Main
class StateItem(Enum):
    NAME = 'name'

    def __str__(self) -> str:
        return self.value
