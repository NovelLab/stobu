"""Define data name of mob file."""

# Official Librarires
from enum import Enum


__all__ = (
        'MobItem',
        'MobType',
        )



class MobItem(Enum):
    TYPE = 'type'
    NAME = 'name'

    def __str__(self) -> str:
        return self.value


class MobType(Enum):
    NONE = 'none'
    MOB = 'mob'
    GENERAL = 'general'

    def __str__(self) -> str:
        return self.value
