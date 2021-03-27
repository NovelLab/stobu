"""Define outline data and record."""

# Official Libraries
from dataclasses import dataclass


# My Modules
from stobu.types.basetypes import _BaseData


__all__ = (
        'OutlineRecord',
        'OutlinesData',
        )


# Main
@dataclass
class OutlineRecord(object):
    title: str
    data: str


class OutlineData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, OutlineRecord)
