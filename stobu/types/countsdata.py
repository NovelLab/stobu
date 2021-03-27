"""Define count data and record."""

# Official Libraries
from dataclasses import dataclass
from enum import Enum, auto


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        'CountRecord',
        'CountRecordType',
        'CountsData',
        )


# Main
class CountRecordType(Enum):
    NONE = auto()


@dataclass
class CountRecord(object):
    type: CountRecordType
    title: str
    total: int
    space: int
    lines: float
    papers: float


class CountsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, CountRecord)
