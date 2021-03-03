"""Define Data types for storybuilder project."""

# annotation magic
from __future__ import annotations

# Official Libraries
from dataclasses import dataclass, field
from typing import Any


# My Modules
from stobu.util import assertion


__all__ = (
        'ActionData',
        'ActionRecord',
        'ContentsData',
        'ContentRecord',
        'CountData',
        'CountRecord',
        'OutlineData',
        'OutlineRecord',
        'OutputData',
        'PlotData',
        'PlotRecord',
        'StoryCode',
        'StoryCodeData',
        'StoryData',
        'StoryRecord',
        )


class _BaseData(object):

    def __init__(self, data: list, rec_type: Any):
        assert isinstance(data, list)
        self.data = [assertion.is_instance(r, rec_type) for r in data]

    def get_data(self) -> list:
        return self.data

    def __add__(self, another: Any) -> _BaseData:
        if isinstance(another, type(self)):
            self.data = self.data + another.data
            return self
        else:
            TypeError("Invalid type!")
            return self


class ActionData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, ActionRecord)


@dataclass
class ActionRecord(object):
    type: str
    subject: str
    action: str = ""
    outline: str = ""
    desc: str = ""
    flags: list = field(default_factory=list)
    note: str = ""


class ContentsData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, ContentRecord)


@dataclass
class ContentRecord(object):
    category: str
    title: str
    index: int


class CountData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, CountRecord)


@dataclass
class CountRecord(object):
    category: str
    title: str
    total: int
    space: int
    lines: float
    papers: float


class OutlineData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, OutlineRecord)


@dataclass
class OutlineRecord(object):
    title: str
    data: str


class OutputData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, str)
        assert isinstance(data, list)

    def get_serialized_data(self) -> str:
        return "".join(self.data)


class PlotData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, PlotRecord)


@dataclass
class PlotRecord(object):
    title: str
    setup: str
    tp1st: str
    develop: str
    tp2nd: str
    climax: str
    resolve: str


@dataclass
class StoryCode(object):
    head: str
    body: str
    foot: Any = None


class StoryCodeData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, StoryCode)


class StoryData(_BaseData):

    def __init__(self, data: list):
        super().__init__(data, StoryRecord)


@dataclass
class StoryRecord(object):
    category: str
    filename: str
    data: dict = field(default_factory=dict)
