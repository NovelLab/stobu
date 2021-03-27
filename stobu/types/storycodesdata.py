"""Define story code data and record."""

# Official Libraries
from dataclasses import dataclass
from typing import Any


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        'StoryCode',
        'StoryCodesData',
        )


# Main
@dataclass
class StoryCode(object):
    head: str
    body: str
    foot: Any = None


class StoryCodesData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, StoryCode)
