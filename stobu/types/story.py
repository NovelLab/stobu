"""Define story data and record."""

# Official Libraries
from dataclasses import dataclass, field


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.element import ElmType


__all__ = (
        'StoryRecord',
        'StoryData',
        )


# Main
@dataclass
class StoryRecord(object):
    type: ElmType
    filename: str
    data: dict = field(default_factory=dict)


class StoryData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, StoryRecord)
