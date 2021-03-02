"""Define Data types for storybuilder project."""


# Official Libraries
from dataclasses import dataclass, field
from typing import Any


# My Modules
from storybuilder.util import assertion


__all__ = (
        'ActionData',
        'ActionRecord',
        'ContentsData',
        'ContentRecord',
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


class ActionData(object):

    def __init__(self, data: list):
        assert isinstance(data, list)
        tmp = []
        for record in data:
            tmp.append(assertion.is_instance(record, ActionRecord))
        self.data = tmp

    def get_data(self) -> list:
        return self.data


@dataclass
class ActionRecord(object):
    type: str
    subject: str
    action: str=""
    outline: str=""
    desc: str=""
    flags: list=field(default_factory=list)
    note: str=""


class ContentsData(object):

    def __init__(self, data: list):
        tmp = []
        for record in data:
            tmp.append(assertion.is_instance(record, ContentRecord))
        self.data = tmp

    def get_data(self) -> list:
        return self.data


@dataclass
class ContentRecord(object):
    category: str
    title: str
    index: int


@dataclass
class CountRecord(object):
    category: str
    title: str
    total: int


class OutlineData(object):

    def __init__(self, data: list):
        assert isinstance(data, list)
        tmp = []
        for record in data:
            tmp.append(assertion.is_instance(record, OutlineRecord))
        self.data = tmp

    def get_data(self) -> list:
        return self.data


@dataclass
class OutlineRecord(object):
    title: str
    data: str


class OutputData(object):

    def __init__(self, data: list):
        assert isinstance(data, list)

        tmp = []
        for line in data:
            tmp.append(assertion.is_str(line))
        self.data = tmp

    def get_data(self) -> list:
        return self.data

    def get_serialized_data(self) -> str:
        return "".join(self.data)


class PlotData(object):

    def __init__(self, data: list):
        assert isinstance(data, list)
        tmp = []
        for record in data:
            tmp.append(assertion.is_instance(record, PlotRecord))
        self.data = tmp

    def get_data(self) -> list:
        return self.data


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
    foot: Any=None


class StoryCodeData(object):

    def __init__(self, data: list):
        assert isinstance(data, list)
        tmp = []
        for record in data:
            tmp.append(assertion.is_instance(record, StoryCode))
        self.data = tmp

    def get_data(self) -> list:
        return self.data


class StoryData(object):

    def __init__(self, data: list):
        assert isinstance(data, list)
        tmp = []
        for record in data:
            tmp.append(assertion.is_instance(record, StoryRecord))
        self.data = tmp

    def get_data(self) -> list:
        return self.data


@dataclass
class StoryRecord(object):
    category: str
    filename: str
    data: dict=field(default_factory=dict)

