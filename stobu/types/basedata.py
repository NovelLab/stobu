"""Define base data types."""

# annotation magic
from __future__ import annotations


# Official Libraries
from typing import Any


# My Modules
from stobu.utils import assertion


__all__ = (
        '_BaseData',
        )


# Main
class _BaseData(object):

    def __init__(self, data: list, record_cls: Any):
        assert isinstance(data, list)
        self.data = [assertion.is_instance(r, record_cls) for r in data]

    def get_data(self) -> list:
        return self.data

    def has_data(self) -> bool:
        return True if self.data else False

    def __add__(self, another: Any) -> _BaseData:
        if isinstance(another, type(self)):
            self.data = self.data + another.data
            return self
        else:
            TypeError("Invalid type!")
            return self
