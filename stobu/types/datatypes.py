"""Define Data types for storybuilder project."""

# annotation magic
from __future__ import annotations

# Official Libraries
from dataclasses import dataclass, field
from typing import Any


# My Modules
from stobu.types.actiontypes import ActRecordType
from stobu.types.storyrecordtypes import StoryRecordType
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





