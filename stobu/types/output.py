"""Define output data and record."""

# Official Libraries
from __future__ import annotations


# My Modules
from stobu.types.basedata import _BaseData


__all__ = (
        'OutputsData',
        )


# Main
class OutputsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, str)

    def get_serialized_data(self) -> str:
        return "".join(self.data)

    def cloned(self) -> OutputsData:
        return OutputsData(self.data)
