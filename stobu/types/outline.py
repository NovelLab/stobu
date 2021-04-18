"""Define outline data and record."""

# Official Libraries
from dataclasses import dataclass


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.element import ElmType


__all__ = (
        'OutlineRecord',
        'OutlinesData',
        )


# Main
@dataclass
class OutlineRecord(object):
    type: ElmType
    title: str
    outline: str


class OutlinesData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, OutlineRecord)
