"""Create templates."""


# Official Libraries
from __future__ import annotations
import os


# My Modules
from stobu.settings import COPYRIGHT, VERSION, DEFAULT_EDITOR
from stobu.settings import YAML_EXT
from stobu.settings import PROJECT_EXT, BOOK_EXT, ORDER_EXT, TODO_EXT, RUBI_EXT
from stobu.settings import TIME_EXT
from stobu.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT
from stobu.settings import PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.settings import PLAN_EXT, OUTLINE_EXT, EVENT_EXT
from stobu.util.fileio import read_file
from stobu.util.filepath import add_extention, is_exists_path
from stobu.util.strings import rid_rn
from stobu.util.log import logger


# Define template file names
PLOT_EXT = YAML_EXT
"""str: extention of plot template file."""

PROJECT_TEMP_FILE = add_extention('project_tmp', PROJECT_EXT)
"""str: file name of project template."""

BOOK_TEMP_FILE = add_extention('book_tmp', BOOK_EXT)
"""str: file name of book template."""

ORDER_TEMP_FILE = add_extention('order_tmp', ORDER_EXT)
"""str: file name of order template."""

CHAPTER_TEMP_FILE = add_extention('chapter_tmp', CHAPTER_EXT)
"""str: file name of chapter template."""

EPISODE_TEMP_FILE = add_extention('episode_tmp', EPISODE_EXT)
"""str: file name of episode template."""

SCENE_TEMP_FILE = add_extention('scene_tmp', SCENE_EXT)
"""str: file name of scene template."""

NOTE_TEMP_FILE = add_extention('note_tmp', NOTE_EXT)
"""str: file name of note template."""

PERSON_TEMP_FILE = add_extention('person_tmp', PERSON_EXT)
"""str: file name of person template."""

STAGE_TEMP_FILE = add_extention('stage_tmp', STAGE_EXT)
"""str: file name of stage template."""

ITEM_TEMP_FILE = add_extention('item_tmp', ITEM_EXT)
"""str: file name of item template."""

WORD_TEMP_FILE = add_extention('word_tmp', WORD_EXT)
"""str: file name of word template."""

PLOT_TEMP_FILE = add_extention('plot_tmp', PLOT_EXT)
"""str: file name of plot template."""

RUBI_TEMP_FILE = add_extention('rubi_tmp', RUBI_EXT)
"""str: file name of rubi template."""

TODO_TEMP_FILE = add_extention('todo_tmp', TODO_EXT)
"""str: file name of todo template."""

TIME_TEMP_FILE = add_extention('time_tmp', TIME_EXT)
"""str: file name of time template."""

PLAN_TEMP_FILE = add_extention('plan_tmp', PLAN_EXT)
"""str: file name of plan template."""

OUTLINE_TEMP_FILE = add_extention('outline_tmp', OUTLINE_EXT)
"""str: file name of outline template."""

EVENT_TEMP_FILE = add_extention('event_tmp', EVENT_EXT)


# Error Messages
ERR_MESSAGE_NOT_FOUND_DATA = "Not found the {target} template data!: %s"
"""str: error message when the file not found."""

ERR_MESSAGE_MISSING_FILE = "Missing the {target} template file path!: %s"
"""str: error message when the file path not found."""


class TemplateCreator(object):

    """Create for project templates."""

    _singleton = None
    """object (TemplateCreater): class instance as singleton."""

    def __init__(self) -> None:
        logger.debug("Initializing TemplateCreater...")
        self._data_path = os.path.join(os.path.dirname(__file__), 'data')
        self._tmps = {
                'project': PROJECT_TEMP_FILE,
                'book': BOOK_TEMP_FILE,
                'order': ORDER_TEMP_FILE,
                'chapter': CHAPTER_TEMP_FILE,
                'episode': EPISODE_TEMP_FILE,
                'scene': SCENE_TEMP_FILE,
                'note': NOTE_TEMP_FILE,
                'person': PERSON_TEMP_FILE,
                'stage': STAGE_TEMP_FILE,
                'item': ITEM_TEMP_FILE,
                'word': WORD_TEMP_FILE,
                'plot': PLOT_TEMP_FILE,
                'rubi': RUBI_TEMP_FILE,
                'todo': TODO_TEMP_FILE,
                'time': TIME_TEMP_FILE,
                'plan': PLAN_TEMP_FILE,
                'outline': OUTLINE_TEMP_FILE,
                'event': EVENT_TEMP_FILE,
                }
        logger.debug("...Success initialized.")

    @classmethod
    def get_instance(cls) -> TemplateCreator:
        """Get the class instance as a singleton."""
        if not cls._singleton:
            logger.debug('> Create and Init the TemplateCreator.')
            cls._singleton = TemplateCreator()
        return cls._singleton

    # methods
    def get_book_template(self) -> str:
        return self._get_template_data('book', True)

    def get_chapter_template(self) -> str:
        return self._get_template_data('chapter', True)

    def get_episode_template(self) -> str:
        return self._get_template_data('episode', True)

    def get_event_template(self) -> str:
        return self._get_template_data('event')

    def get_item_template(self) -> str:
        return self._get_template_data('item')

    def get_note_template(self) -> str:
        return self._get_template_data('note')

    def get_order_template(self) -> str:
        return self._get_template_data('order')

    def get_outline_template(self) -> str:
        return self._get_template_data('outline')

    def get_person_template(self) -> str:
        return self._get_template_data('person')

    def get_plan_template(self) -> str:
        return self._get_template_data('plan')

    def get_project_template(self) -> str:
        path = os.path.join(self._data_path, self._tmps['project'])
        tmp = read_file(path)
        if tmp:
            return tmp.replace('{VERSION}', VERSION).replace(
                    '{COPYRIGHT}', COPYRIGHT).replace(
                            '{EDITOR}', DEFAULT_EDITOR)
        else:
            logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target="project"), tmp)
            return ""

    def get_rubi_template(self) -> str:
        return self._get_template_data('rubi')

    def get_scene_template(self) -> str:
        return self._get_template_data('scene', True)

    def get_stage_template(self) -> str:
        return self._get_template_data('stage')

    def get_todo_template(self) -> str:
        return self._get_template_data('todo')

    def get_time_template(self) -> str:
        return self._get_template_data('time')

    def get_word_template(self) -> str:
        return self._get_template_data('word')


    # Private Methods
    def _get_template_data(self, title: str, with_plot: bool = False) -> str:
        assert isinstance(title, str)
        assert title in self._tmps

        path = os.path.join(self._data_path, self._tmps[title])
        if not is_exists_path(path):
            logger.warning(ERR_MESSAGE_MISSING_FILE.format(target=title), path)
            return ""

        tmp = read_file(path)
        if with_plot:
            plot = read_file(os.path.join(self._data_path, self._tmps['plot']))
            if tmp and plot:
                return tmp.replace('{PLOT}', rid_rn(plot))
            else:
                logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target=title))
                return ""
        else:
            if tmp:
                return tmp
            else:
                logger.warning(ERR_MESSAGE_NOT_FOUND_DATA.format(target=title))
                return ""
