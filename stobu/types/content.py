"""Define contents data and record."""

# Official Libraries
from dataclasses import dataclass, field
from enum import auto, Enum


# My Modules
from stobu.types.basedata import _BaseData
from stobu.types.element import ElmType


__all__ = (
        'ContentRecord',
        'ContentsData',
        )


# Main
@dataclass
class ContentRecord(object):
    type: ElmType
    title: str
    index: int


class ContentsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, ContentRecord)
