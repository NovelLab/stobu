"""Define count data and record."""

# Official Libraries
from dataclasses import dataclass


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.element import ElmType


__all__ = (
        'CountRecord',
        'CountsData',
        )


# Main
@dataclass
class CountRecord(object):
    type: ElmType
    title: str
    total: int
    space: int
    lines: float
    papers: float


class CountsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, CountRecord)
