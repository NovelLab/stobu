"""Define project paths."""

# Official Libraries


# My Modules
from stobu import __app_base_dir__
from stobu import __project_path__
from stobu.types.element import ElmType


# Define Constants
APP_DIR = __app_base_dir__
"""str: path of application directory."""

PROJECT_DIR = __project_path__
"""str: path of project directory."""

MARKDOWN_EXT = 'md'
"""str: extention of markdown files."""

TEXT_EXT = 'txt'
"""str: extention of text files."""

YAML_EXT = 'yml'
"""str: extention of yaml files."""


DIRS_TABLE = {
        ElmType.BOOK: '',
        ElmType.BUILD: 'build',
        ElmType.CHAPTER: 'chapters',
        ElmType.EPISODE: 'episodes',
        ElmType.EVENT: 'events',
        ElmType.ITEM: 'items',
        ElmType.MATERIAL: 'materials',
        ElmType.MOB: '',
        ElmType.NONE: '',
        ElmType.NOTE: 'notes',
        ElmType.ORDER: '',
        ElmType.OUTLINE: 'outlines',
        ElmType.PERSON: 'persons',
        ElmType.PLAN: 'plans',
        ElmType.PLOT: '',
        ElmType.PROJECT: '',
        ElmType.RUBI: '',
        ElmType.SCENE: 'scenes',
        ElmType.STAGE: 'stages',
        ElmType.TIME: '',
        ElmType.TODO: '',
        ElmType.TRASH: '.trash',
        ElmType.WORD: 'words',
        }


BASE_FILE_TABLE = {
        ElmType.BOOK: 'book',
        ElmType.BUILD: '',
        ElmType.CHAPTER: '',
        ElmType.EPISODE: '',
        ElmType.EVENT: '',
        ElmType.ITEM: '',
        ElmType.MATERIAL: '',
        ElmType.MOB: 'mob',
        ElmType.NONE: '',
        ElmType.NOTE: '',
        ElmType.ORDER: 'order',
        ElmType.OUTLINE: '',
        ElmType.PERSON: '',
        ElmType.PLAN: '',
        ElmType.PLOT: '',
        ElmType.PROJECT: 'project',
        ElmType.RUBI: 'rubi',
        ElmType.SCENE: '',
        ElmType.STAGE: '',
        ElmType.TIME: 'time',
        ElmType.TODO: 'todo',
        ElmType.TRASH: '',
        ElmType.WORD: '',
        }


EXT_TABLE = {
        ElmType.BOOK: YAML_EXT,
        ElmType.BUILD: MARKDOWN_EXT,
        ElmType.CHAPTER: MARKDOWN_EXT,
        ElmType.EPISODE: MARKDOWN_EXT,
        ElmType.EVENT: MARKDOWN_EXT,
        ElmType.ITEM: MARKDOWN_EXT,
        ElmType.MATERIAL: MARKDOWN_EXT,
        ElmType.MOB: YAML_EXT,
        ElmType.NONE: MARKDOWN_EXT,
        ElmType.NOTE: MARKDOWN_EXT,
        ElmType.ORDER: YAML_EXT,
        ElmType.OUTLINE: MARKDOWN_EXT,
        ElmType.PERSON: MARKDOWN_EXT,
        ElmType.PLAN: MARKDOWN_EXT,
        ElmType.PLOT: MARKDOWN_EXT,
        ElmType.PROJECT: YAML_EXT,
        ElmType.RUBI: YAML_EXT,
        ElmType.SCENE: MARKDOWN_EXT,
        ElmType.STAGE: MARKDOWN_EXT,
        ElmType.TIME: YAML_EXT,
        ElmType.TODO: MARKDOWN_EXT,
        ElmType.TRASH: MARKDOWN_EXT,
        ElmType.WORD: MARKDOWN_EXT,
        }
