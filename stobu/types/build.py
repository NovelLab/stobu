"""Define enum type for build command."""

# Official Libraries
from enum import Enum


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
    STRUCT = 'struct'
    SCENE_INFO = 'sceneinfo'
    STATUS_INFO = 'statusinfo'

    def __str__(self):
        return self.value
