"""Define data name of project file."""

# Official Libraries
from enum import Enum


__all__ = (
        'ProjectItem',
        )


class ProjectItem(Enum):
    VERSION = 'version'
    COPYRIGHT = 'copyright'
    EDITOR = 'editor'

    def __str__(self) -> str:
        return self.value
