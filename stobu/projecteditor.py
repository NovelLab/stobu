"""Edit module for storybuilder project."""


# Official Libraries
import argparse
import subprocess


# My Modules
from stobu import projectfilechecker as checker
from stobu.settings import EDITOR
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.filepath import get_input_filename
from stobu.util.log import logger


__all__ = (
        'switch_command_to_edit',
        )


# Define Constants
INPUT_TARGET_FILENAME_WITH_LIST_MESSAGE = "{target_list}\nEnter {target} file name: "
"""str: message to get the deleting file name."""

START_EDIT_PROCESS_MESSAGE = "Editing the {target} file..."
"""str: message to start editing process."""

FINISH_EDIT_PROCESS_MESSAGE = "...Succeeded edit {target} file."
"""str: message to finish the editing process as successfull."""

ERR_MESSAGE_MISSING_FILE = "Not Found the {target} file!: %s"
"""str: error message when the file not found."""

ERR_MESSAGE_CANNOT_EDIT = "Failed to edit the {target} file!: %s"
"""str: error message when the file cannot edit."""


# Main Function
def switch_command_to_edit(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('e', 'edit')

    is_succeeded = False

    if cmdargs.arg0 in ('b', 'book'):
        is_succeeded = edit_the_book()
    elif cmdargs.arg0 in ('o', 'order'):
        is_succeeded = edit_the_order()
    elif cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = edit_the_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = edit_the_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = edit_the_scene(cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = edit_the_note(cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = edit_the_person(cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = edit_the_stage(cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = edit_the_item(cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = edit_the_word(cmdargs.arg1)
    else:
        logger.error("Unknown edit command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command edit!")
        return False

    logger.debug("...Succeeded command edit.")
    return True


# Functions
def edit_the_book() -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="book"))

    if not checker.exists_book_file():
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="book"), "")
        return False

    if not _edit_the_file(ppath.get_book_path()):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="book"), "")
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="book"))
    return True


def edit_the_chapter(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="chapter"))

    chapters = ppath.get_chapter_file_names()
    _fname = _get_target_filename(fname, "editing chapter", chapters)

    if not checker.is_exists_the_chapter(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    if not _edit_the_file(ppath.get_chapter_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="chapter"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="chapter"))
    return True


def edit_the_episode(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="episode"))

    episodes = ppath.get_episode_file_names()
    _fname = _get_target_filename(fname, "editing episode", episodes)

    if not checker.is_exists_the_episode(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    if not _edit_the_file(ppath.get_episode_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="episode"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="episode"))
    return True


def edit_the_item(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="item"))

    items = ppath.get_item_file_names()
    _fname = _get_target_filename(fname, "editing item", items)

    if not checker.is_exists_the_item(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="item"), _fname)
        return False

    if not _edit_the_file(ppath.get_item_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="item"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="item"))
    return True


def edit_the_note(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="note"))

    notes = ppath.get_note_file_names()
    _fname = _get_target_filename(fname, "editing note", notes)

    if not checker.is_exists_the_note(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="note"), _fname)
        return False

    if not _edit_the_file(ppath.get_note_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="note"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="note"))
    return True


def edit_the_order() -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="order"))

    if not checker.exists_order_file():
        logger.error(ERR_MESSAGE_MISSING_FILE.format("order"), "")
        return False

    if not _edit_the_file(ppath.get_order_path()):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="order"), "")
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="order"))
    return True


def edit_the_person(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="person"))

    persons = ppath.get_person_file_names()
    _fname = _get_target_filename(fname, "editing person", persons)

    if not checker.is_exists_the_person(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="person"), _fname)
        return False

    if not _edit_the_file(ppath.get_person_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="person"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="person"))
    return True


def edit_the_scene(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="scene"))

    scenes = ppath.get_scene_file_names()
    _fname = _get_target_filename(fname, "editing scene", scenes)

    if not checker.is_exists_the_scene(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    if not _edit_the_file(ppath.get_scene_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="scene"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="scene"))
    return True


def edit_the_stage(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="stage"))

    stages = ppath.get_stage_file_names()
    _fname = _get_target_filename(fname, "editing stage", stages)

    if not checker.is_exists_the_stage(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="stage"), _fname)
        return False

    if not _edit_the_file(ppath.get_stage_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="stage"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="stage"))
    return True


def edit_the_word(fname: str) -> bool:
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="word"))

    words = ppath.get_word_file_names()
    _fname = _get_target_filename(fname, "editing word", words)

    if not checker.is_exists_the_word(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="word"), _fname)
        return False

    if not _edit_the_file(ppath.get_word_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="word"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="word"))
    return True


# Private Functions
def _edit_the_file(fname: str) -> bool:
    proc = subprocess.run([EDITOR, fname])
    if proc.returncode != 0:
        logger.error("Subprocess Error!: %s", proc.returncode)
        return False
    return True


def _get_target_filename(fname: str, msg: str, targets: list) -> str:
    tmp = []
    idx = 0
    for t in targets:
        tmp.append(f"{idx}:{t}")
        idx += 1
    _fname = assertion.is_str(fname) if fname else get_input_filename(
            INPUT_TARGET_FILENAME_WITH_LIST_MESSAGE.format(target=msg, target_list=" ".join(tmp)))
    if _fname.isnumeric():
        if 0 <= int(_fname) < len(targets):
            return targets[int(_fname)]
        else:
            return _fname
    else:
        return _fname
