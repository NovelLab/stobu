"""Define base info data and record."""

# Official Libraries
from dataclasses import dataclass
from enum import auto, Enum


# My Modules
from stobu.types.basedata import _BaseData


__all__ = (
        'BaseInfoRecord',
        'BaseInfoData',
        'BaseInfoType',
        )


# Main
class BaseInfoType(Enum):
    NONE = auto()


@dataclass
class BaseInfoRecord(object):
    type: BaseInfoType
    info: str


class BaseInfoData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, BaseInfoRecord)
