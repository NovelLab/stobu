"""Create templates."""


# Official Libraries
from __future__ import annotations
import os


# My Modules
from stobu.settings import COPYRIGHT, VERSION, DEFAULT_EDITOR
from stobu.util.fileio import read_file
from stobu.util.log import logger


# Define template file names
PROJECT_TEMP_FILE = 'project_tmp.yml'
"""str: file name of project template."""

BOOK_TEMP_FILE = 'book_tmp.yml'
"""str: file name of book template."""

ORDER_TEMP_FILE = 'order_tmp.yml'
"""str: file name of order template."""

CHAPTER_TEMP_FILE = 'chapter_tmp.yml'
"""str: file name of chapter template."""

EPISODE_TEMP_FILE = 'episode_tmp.yml'
"""str: file name of episode template."""

SCENE_TEMP_FILE = 'scene_tmp.md'
"""str: file name of scene template."""

NOTE_TEMP_FILE = 'note_tmp.md'
"""str: file name of note template."""

PERSON_TEMP_FILE = 'person_tmp.yml'
"""str: file name of person template."""

STAGE_TEMP_FILE = 'stage_tmp.yml'
"""str: file name of stage template."""

ITEM_TEMP_FILE = 'item_tmp.yml'
"""str: file name of item template."""

WORD_TEMP_FILE = 'word_tmp.yml'
"""str: file name of word template."""

PLOT_TEMP_FILE = 'plot_tmp.yml'
"""str: file name of plot template."""

RUBI_TEMP_FILE = 'rubi_tmp.yml'
"""str: file name of rubi template."""

TODO_TEMP_FILE = 'todo_tmp.md'
"""str: file name of todo template."""

PLAN_TEMP_FILEW = 'plan_tmp.md'
"""str: file name of plan template."""

OUTLINE_TEMP_FILE = 'outline_tmp.md'
"""str: file name of outline template."""


# Error Messages
ERR_MESSAGE_NOT_FOUND_DATA = "Not found the {target} template data!: %s"
"""str: error message when the file not found."""


class TemplateCreator(object):

    """Create for project templates."""

    _singleton = None
    """object (TemplateCreater): class instance as singleton."""

    def __init__(self) -> None:
        logger.debug("Initializing TemplateCreater...")
        data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.project_tmp = os.path.join(data_path, PROJECT_TEMP_FILE)
        self.book_tmp = os.path.join(data_path, BOOK_TEMP_FILE)
        self.order_tmp = os.path.join(data_path, ORDER_TEMP_FILE)
        self.chapter_tmp = os.path.join(data_path, CHAPTER_TEMP_FILE)
        self.episode_tmp = os.path.join(data_path, EPISODE_TEMP_FILE)
        self.scene_tmp = os.path.join(data_path, SCENE_TEMP_FILE)
        self.note_tmp = os.path.join(data_path, NOTE_TEMP_FILE)
        self.person_tmp = os.path.join(data_path, PERSON_TEMP_FILE)
        self.stage_tmp = os.path.join(data_path, STAGE_TEMP_FILE)
        self.item_tmp = os.path.join(data_path, ITEM_TEMP_FILE)
        self.word_tmp = os.path.join(data_path, WORD_TEMP_FILE)
        self.plot_tmp = os.path.join(data_path, PLOT_TEMP_FILE)
        self.rubi_tmp = os.path.join(data_path, RUBI_TEMP_FILE)
        self.todo_tmp = os.path.join(data_path, TODO_TEMP_FILE)
        self.plan_tmp = os.path.join(data_path, PLAN_TEMP_FILEW)
        self.outline_tmp = os.path.join(data_path, OUTLINE_TEMP_FILE)
        logger.debug("...Success initialized.")

    @classmethod
    def get_instance(cls) -> TemplateCreator:
        """Get the class instance as a singleton."""
        if not cls._singleton:
            cls._singleton = TemplateCreator()
        return cls._singleton

    # methods
    def get_book_template(self) -> str:
        tmp = read_file(self.book_tmp)
        plot = read_file(self.plot_tmp)
        if tmp and plot:
            return tmp.replace('{PLOT}', plot.rstrip('\n\r'))
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="book"), tmp)
            return ""

    def get_chapter_template(self) -> str:
        tmp = read_file(self.chapter_tmp)
        plot = read_file(self.plot_tmp)
        if tmp and plot:
            return tmp.replace('{PLOT}', plot.rstrip('\n\r'))
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="chapter"), tmp)
            return ""

    def get_episode_template(self) -> str:
        tmp = read_file(self.episode_tmp)
        plot = read_file(self.plot_tmp)
        if tmp and plot:
            return tmp.replace('{PLOT}', plot.rstrip('\n\r'))
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="episode"), tmp)
            return ""

    def get_item_template(self) -> str:
        tmp = read_file(self.item_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="item"), tmp)
            return ""

    def get_note_template(self) -> str:
        tmp = read_file(self.note_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="note"), tmp)
            return ""

    def get_order_template(self) -> str:
        tmp = read_file(self.order_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="order"), tmp)
            return ""

    def get_outline_template(self) -> str:
        tmp = read_file(self.outline_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="outline"), tmp)
            return ""

    def get_person_template(self) -> str:
        tmp = read_file(self.person_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="person"), tmp)
            return ""

    def get_plan_template(self) -> str:
        tmp = read_file(self.plan_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="plan"), tmp)
            return ""

    def get_project_template(self) -> str:
        tmp = read_file(self.project_tmp)
        if tmp:
            return tmp.replace('{VERSION}', VERSION).replace(
                    '{COPYRIGHT}', COPYRIGHT).replace(
                            '{EDITOR}', DEFAULT_EDITOR)
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="project"), tmp)
            return ""

    def get_rubi_template(self) -> str:
        tmp = read_file(self.rubi_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="rubi"), tmp)
            return ""

    def get_scene_template(self) -> str:
        tmp = read_file(self.scene_tmp)
        plot = read_file(self.plot_tmp)
        if tmp and plot:
            return tmp.replace('{PLOT}', plot.rstrip('\n\r'))
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="scene"), tmp)
            return ""

    def get_stage_template(self) -> str:
        tmp = read_file(self.stage_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="stage"), tmp)
            return ""

    def get_todo_template(self) -> str:
        tmp = read_file(self.todo_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="todo"), tmp)
            return ""

    def get_word_template(self) -> str:
        tmp = read_file(self.word_tmp)
        if tmp:
            return tmp
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="word"), tmp)
            return ""
