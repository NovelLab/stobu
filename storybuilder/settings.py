"""Internal settings for storybuilder."""


# Official Libraries


# My Modules
from storybuilder import __version__


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

CHAPTER_DIR = 'chapters'
"""str: directory name for chapter files."""

EPISODE_DIR = 'episodes'
"""str: directory name for episode files."""

SCENE_DIR = 'scenes'
"""str: directory name for scene files."""

NOTE_DIR = 'notes'
"""str: directory name for note files."""

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

BUILD_DIR = 'build'
"""str: directory name for build."""

CHAPTER_EXT = YAML_EXT
"""str: extention of chapter files."""

EPISODE_EXT = YAML_EXT
"""str: extention of episode files."""

SCENE_EXT = MARKDOWN_EXT
"""str: extention of scene files."""

NOTE_EXT = MARKDOWN_EXT
"""str: extention of note files."""

PERSON_EXT = YAML_EXT
"""str: extention of person files."""

STAGE_EXT = YAML_EXT
"""str: extention of stage files."""

ITEM_EXT = YAML_EXT
"""str: extention of item files."""

WORD_EXT = YAML_EXT
"""str: extention of word files."""

BASE_ENCODING = 'utf-8'
"""str: basic file encoding type."""

EDITOR = 'vim'
"""str: editor for the application."""
