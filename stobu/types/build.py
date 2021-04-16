"""Define enum type for build command."""

# Official Libraries
from enum import auto, Enum


__all__ = (
        'BuildType',
        )


class BuildType(Enum):
    NONE = 'none'
    BASE = 'base'
    NOVEL = 'novel'
    OUTLINE = 'outline'
    PLOT = 'plot'
    SCRIPT = 'script'

    def __str__(self):
        return self.value