"""Internal settings for storybuilder."""


# Official Libraries


# My Modules
from stobu import __version__


# Define Basic Info
PROJECT = "StoryBuilder"
"""str: application name."""

VERSION = __version__
"""str: application version."""

COPYRIGHT = "(c)2020,2021 N.T.WORKS"
"""str: application copyright."""

AUTHORS = ["N.T.WORKS"]
"""list[str]: application authors."""


# Define Shared Info
MARKDOWN_EXT = 'md'
"""str: extention of MARKDOWN files."""

YAML_EXT = 'yml'
"""str: extention of YAML files."""

PROJECT_FILENAME = f"project.{YAML_EXT}"
"""str: file name of project file."""

BOOK_FILENAME = f"book.{YAML_EXT}"
"""str: file name of book file."""

ORDER_FILENAME = f"order.{YAML_EXT}"
"""str: file name of order file."""

RUBI_FILENAME = f"rubi.{YAML_EXT}"
"""str: file name of rubi file."""

TODO_FILENAME = f"todo.{MARKDOWN_EXT}"
"""str: file name of todo file."""

CHAPTER_DIR = 'chapters'
"""str: directory name for chapter files."""

EPISODE_DIR = 'episodes'
"""str: directory name for episode files."""

SCENE_DIR = 'scenes'
"""str: directory name for scene files."""

NOTE_DIR = 'notes'
"""str: directory name for note files."""

PLAN_DIR = 'plans'
"""str: directory name for plan files."""

OUTLINE_DIR = 'outlines'
"""str: directory name for outline files."""

PERSON_DIR = 'persons'
"""str: directory name for person files."""

STAGE_DIR = 'stages'
"""str: directory name for stage files."""

ITEM_DIR = 'items'
"""str: directory name for item files."""

WORD_DIR = 'words'
"""str: directory name for word files."""

TRASH_DIR = '.trash'
"""str: directory name for trash box."""

MATERIAL_DIR = 'materials'
"""str: directory name for materials."""

EVENT_DIR = 'events'
"""str: directory name for events."""

BUILD_DIR = 'build'
"""str: directory name for build."""

PROJECT_EXT = YAML_EXT
"""str: extention of project file."""

BOOK_EXT = YAML_EXT
"""str: extention of book file."""

ORDER_EXT = YAML_EXT
"""str: extention of order file."""

TODO_EXT = MARKDOWN_EXT
"""str: extention of todo file."""

RUBI_EXT = YAML_EXT
"""str: extention of rubi file."""

CHAPTER_EXT = MARKDOWN_EXT
"""str: extention of chapter files."""

EPISODE_EXT = MARKDOWN_EXT
"""str: extention of episode files."""

SCENE_EXT = MARKDOWN_EXT
"""str: extention of scene files."""

NOTE_EXT = MARKDOWN_EXT
"""str: extention of note files."""

PLAN_EXT = MARKDOWN_EXT
"""str: extention of plan files."""

OUTLINE_EXT = MARKDOWN_EXT
"""str: extention of outline files."""

EVENT_EXT = MARKDOWN_EXT
"""str: extention of event files."""

PERSON_EXT = MARKDOWN_EXT
"""str: extention of person files."""

STAGE_EXT = MARKDOWN_EXT
"""str: extention of stage files."""

ITEM_EXT = MARKDOWN_EXT
"""str: extention of item files."""

WORD_EXT = MARKDOWN_EXT
"""str: extention of word files."""

BASE_ENCODING = 'utf-8'
"""str: basic file encoding type."""

DEFAULT_EDITOR = 'vim'
"""str: editor for the application."""
