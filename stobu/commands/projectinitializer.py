"""Initialize module for storybuilder's project."""


# Official Libraries
import os
from typing import Callable


# My Modules
from stobu.settings import PROJECT_FILENAME, BOOK_FILENAME, ORDER_FILENAME, RUBI_FILENAME
from stobu.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT, PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.settings import BUILD_DIR, CHAPTER_DIR, EPISODE_DIR, SCENE_DIR, NOTE_DIR, PERSON_DIR, STAGE_DIR, ITEM_DIR, WORD_DIR, TRASH_DIR
from stobu.settings import PLAN_DIR, OUTLINE_DIR, MATERIAL_DIR, EVENT_DIR
from stobu.templatecreator import TemplateCreator
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util.fileio import write_file
from stobu.util.filepath import get_current_path, is_exists_path
from stobu.util.log import logger


__all__ = (
        'init_project',
        )


# Define Constants
ERR_ALREADY_EXISTS = '> Already exists the {target}!: %s'
"""str: error message template when the file or directory exists."""

ERR_CHECK_AND_CREATE = '...Failed the check or create {target}!: %s'
"""str: error message template for check or create any."""

ERR_CREATE_FILE = '...Failed the create {}!: %s'
"""str: error message template when cannot create the file."""

ERR_MISSING_TEMPLATE_DATA = '> Missing the {target} template data!: %s'
"""str: error message template when missing the template data."""

FINISH_PROCESS_CHECK_AND_CREATE = '...Succeeded the check and create {target}.'
"""str: message template for finish process to check and create any."""

FINISH_PROCESS_CREATE_FILE = '...Succeeded to create the {target} file.'
"""str: message template for finish process to create the file."""

START_PROCESS_CHECK_AND_CREATE = 'Starting the check and create {target}...'
"""str: message template for start process to check and create any."""

START_PROCESS_CREATE_FILE = 'Starting to create the {target} file...'
"""str: message template for start process to create the file."""


# Main Function
def init_project() -> bool:
    logger.debug("Starting Project Initializer...")

    creator = TemplateCreator.get_instance()
    if not creator:
        logger.error("Missing TemplateCreator. not initialized!: %s", creator)
        return False

    if not _check_and_create_the_file_using_template(
            'project', ppath.get_project_path(),
            checker.exists_project_file, creator.get_project_template):
        logger.debug("Failure creating the project file!")
        return False

    if not check_and_create_defaults(creator):
        logger.error("Failed check and create defaults!")
        return False

    logger.debug("...Succeeded init project.")
    return True


# Functions
def check_and_create_defaults(creator: TemplateCreator) -> bool:
    logger.debug("Starting the check and create default dir and files...")
    assert isinstance(creator, TemplateCreator)

    if not check_and_create_default_dirs():
        logger.error("Failed the check and create default directories!")
        return False

    if not check_and_create_default_files(creator):
        logger.error("Failed the check and create default files!")
        return False

    logger.debug("...Succeeded the check and create defaults.")
    return True


def check_and_create_default_dirs() -> bool:
    logger.debug("Starting the check and create default directories...")

    if not _check_and_create_dir('chapter', CHAPTER_DIR) \
            or not _check_and_create_dir('episode', EPISODE_DIR) \
            or not _check_and_create_dir('scene', SCENE_DIR) \
            or not _check_and_create_dir('note', NOTE_DIR) \
            or not _check_and_create_dir('person', PERSON_DIR) \
            or not _check_and_create_dir('stage', STAGE_DIR) \
            or not _check_and_create_dir('item', ITEM_DIR) \
            or not _check_and_create_dir('word', WORD_DIR) \
            or not _check_and_create_dir('trash', TRASH_DIR) \
            or not _check_and_create_dir('material', MATERIAL_DIR) \
            or not _check_and_create_dir('plan', PLAN_DIR) \
            or not _check_and_create_dir('outline', OUTLINE_DIR) \
            or not _check_and_create_dir('event', EVENT_DIR) \
            or not _check_and_create_dir('build', BUILD_DIR):
        logger.error("Failed check and create default dirs!")
        return False

    logger.debug("...Succeeded check and create default directories.")
    return True


def check_and_create_default_files(creator: TemplateCreator) -> bool:
    logger.debug("Starting the check and create default files...")
    assert isinstance(creator, TemplateCreator)

    if not _check_and_create_the_file_using_template(
            'book', ppath.get_book_path(),
            checker.exists_book_file, creator.get_book_template) \
            or not _check_and_create_the_file_using_template(
                    'order', ppath.get_order_path(),
                    checker.exists_order_file, creator.get_order_template) \
            or not _check_and_create_the_file_using_template(
                    'rubi', ppath.get_rubi_path(),
                    checker.exists_rubi_file, creator.get_rubi_template) \
            or not _check_and_create_the_file_using_template(
                    'todo', ppath.get_todo_path(),
                    checker.exists_todo_file, creator.get_todo_template) \
            or not _check_and_create_the_file_using_template(
                    'time', ppath.get_time_path(),
                    checker.exists_time_file, creator.get_time_template) \
            or not _check_and_create_the_file_using_template(
                    'chapter', ppath.get_chapter_path('main'),
                    checker.exists_any_chapter, creator.get_chapter_template) \
            or not _check_and_create_the_file_using_template(
                    'episode', ppath.get_episode_path('main'),
                    checker.exists_any_episode, creator.get_episode_template) \
            or not _check_and_create_the_file_using_template(
                    'scene', ppath.get_scene_path('main'),
                    checker.exists_any_scene, creator.get_scene_template) \
            or not _check_and_create_the_file_using_template(
                    'note', ppath.get_note_path('main'),
                    checker.exists_any_note, creator.get_note_template) \
            or not _check_and_create_the_file_using_template(
                    'plan', ppath.get_plan_path('main'),
                    checker.exists_any_plan, creator.get_plan_template) \
            or not _check_and_create_the_file_using_template(
                    'outline', ppath.get_outline_path('main'),
                    checker.exists_any_outline, creator.get_outline_template) \
            or not _check_and_create_the_file_using_template(
                    'event', ppath.get_event_path('main'),
                    checker.exists_any_event, creator.get_event_template) \
            or not _check_and_create_the_file_using_template(
                    'person', ppath.get_person_path('main'),
                    checker.exists_any_person, creator.get_person_template) \
            or not _check_and_create_the_file_using_template(
                    'stage', ppath.get_stage_path('main'),
                    checker.exists_any_stage, creator.get_stage_template) \
            or not _check_and_create_the_file_using_template(
                    'item', ppath.get_item_path('main'),
                    checker.exists_any_item, creator.get_item_template) \
            or not _check_and_create_the_file_using_template(
                    'word', ppath.get_word_path('main'),
                    checker.exists_any_word, creator.get_word_template):
        logger.error("Failed check and create default files!")
        return False

    logger.debug("...Succeeded the check and create default files.")
    return True


# Private Functions
def _check_and_create_dir(target: str, dir_name: str) -> bool:
    assert isinstance(target, str)
    assert isinstance(dir_name, str)

    _target = f"{target} directory"
    logger.debug(START_PROCESS_CHECK_AND_CREATE.format(target=_target))

    path = os.path.join(get_current_path(), dir_name)
    if not _safe_create_directory(path):
        logger.error(ERR_CHECK_AND_CREATE.format(target=_target), path)
        return False

    logger.debug(FINISH_PROCESS_CHECK_AND_CREATE.format(target=_target))
    return True


def _check_and_create_the_file_using_template(target: str, path: str,
        check_method: Callable, create_method: Callable) -> bool:
    assert isinstance(target, str)
    assert isinstance(path, str)
    assert callable(check_method)
    assert callable(create_method)
    logger.debug(START_PROCESS_CREATE_FILE.format(target=target))

    if check_method():
        logger.debug(ERR_ALREADY_EXISTS.format(target=f"{target} file"), path)
        return True

    template_data = create_method()
    if not template_data:
        logger.error(ERR_MISSING_TEMPLATE_DATA.format(target=target), template_data)
        return False

    if not write_file(path, template_data):
        logger.error(ERR_CREATE_FILE.format(target=target), path)
        return False

    logger.debug(FINISH_PROCESS_CREATE_FILE.format(target=target))
    return True


def _safe_create_directory(dirname: str) -> bool:
    """Check and create a directory."""

    if not is_exists_path(dirname):
        os.makedirs(dirname)
    else:
        logger.debug("> Already exists the directory: %s", dirname)

    return True
