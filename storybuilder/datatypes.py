"""Define Data types for storybuilder project."""


# Official Libraries
from dataclasses import dataclass, field
from typing import Any


# My Modules


@dataclass
class ActionRecord(object):
    type: str
    subject: str
    action: str=""
    outline: str=""
    desc: str=""
    flags: list=field(default_factory=list)
    note: str=""


@dataclass
class ContentRecord(object):
    category: str
    title: str
    index: int


@dataclass
class OutlineRecord(object):
    title: str
    data: str


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


@dataclass
class StoryRecord(object):
    category: str
    filename: str
    data: dict=field(default_factory=dict)

