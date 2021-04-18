"""Define plot data and record."""

# Official Libraries
from dataclasses import dataclass


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.element import ElmType


__all__ = (
        'PlotRecord',
        'PlotsData',
        )


# Main
@dataclass
class PlotRecord(object):
    type: ElmType
    title: str
    setup: str
    tp1st: str
    develop: str
    tp2nd: str
    climax: str
    resolve: str


class PlotsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, PlotRecord)
