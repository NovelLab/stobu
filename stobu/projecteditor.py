"""Edit module for storybuilder project."""


# Official Libraries
import argparse
import subprocess


# My Modules
from stobu.dataconverter import conv_to_dumpdata_of_yaml
from stobu.settings import DEFAULT_EDITOR
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import read_file_as_yaml, write_file
from stobu.util.filepath import get_input_filename
from stobu.util.log import logger


__all__ = (
        'switch_command_to_edit',
        'switch_command_to_set_editor',
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

    editor = assertion.is_str(_get_editor())

    if cmdargs.arg0 in ('b', 'book'):
        is_succeeded = edit_the_book(editor)
    elif cmdargs.arg0 in ('o', 'order'):
        is_succeeded = edit_the_order(editor)
    elif cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = edit_the_chapter(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = edit_the_episode(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = edit_the_scene(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = edit_the_note(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = edit_the_person(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = edit_the_stage(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = edit_the_item(editor, cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = edit_the_word(editor, cmdargs.arg1)
    else:
        logger.error("Unknown edit command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command edit!")
        return False

    logger.debug("...Succeeded command edit.")
    return True


def switch_command_to_set_editor(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd == 'set_editor'
    logger.debug("Setting the project Editor...")

    editor = cmdargs.arg0 if cmdargs.arg0 else input("Please set the Editor name: ")
    proj_data = read_file_as_yaml(ppath.get_project_path())
    proj_data['storybuilder']['editor'] = editor

    if not write_file(ppath.get_project_path(), conv_to_dumpdata_of_yaml(proj_data)):
        logger.error("...Failed to set the editor!: %s", editor)
        return False

    return True


# Functions
def edit_the_book(editor: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="book"))

    if not checker.exists_book_file():
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="book"), "")
        return False

    if not _edit_the_file(editor, ppath.get_book_path()):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="book"), "")
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="book"))
    return True


def edit_the_chapter(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="chapter"))

    chapters = ppath.get_chapter_file_names()
    _fname = _get_target_filename(fname, "editing chapter", chapters)

    if not checker.is_exists_the_chapter(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_chapter_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="chapter"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="chapter"))
    return True


def edit_the_episode(editor: str, fnae: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="episode"))

    episodes = ppath.get_episode_file_names()
    _fname = _get_target_filename(fname, "editing episode", episodes)

    if not checker.is_exists_the_episode(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_episode_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="episode"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="episode"))
    return True


def edit_the_item(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="item"))

    items = ppath.get_item_file_names()
    _fname = _get_target_filename(fname, "editing item", items)

    if not checker.is_exists_the_item(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="item"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_item_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="item"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="item"))
    return True


def edit_the_note(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="note"))

    notes = ppath.get_note_file_names()
    _fname = _get_target_filename(fname, "editing note", notes)

    if not checker.is_exists_the_note(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="note"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_note_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="note"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="note"))
    return True


def edit_the_order(editor: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="order"))

    if not checker.exists_order_file():
        logger.error(ERR_MESSAGE_MISSING_FILE.format("order"), "")
        return False

    if not _edit_the_file(editor, ppath.get_order_path()):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="order"), "")
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="order"))
    return True


def edit_the_person(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="person"))

    persons = ppath.get_person_file_names()
    _fname = _get_target_filename(fname, "editing person", persons)

    if not checker.is_exists_the_person(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="person"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_person_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="person"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="person"))
    return True


def edit_the_scene(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="scene"))

    scenes = ppath.get_scene_file_names()
    _fname = _get_target_filename(fname, "editing scene", scenes)

    if not checker.is_exists_the_scene(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_scene_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="scene"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="scene"))
    return True


def edit_the_stage(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="stage"))

    stages = ppath.get_stage_file_names()
    _fname = _get_target_filename(fname, "editing stage", stages)

    if not checker.is_exists_the_stage(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="stage"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_stage_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="stage"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="stage"))
    return True


def edit_the_word(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target="word"))

    words = ppath.get_word_file_names()
    _fname = _get_target_filename(fname, "editing word", words)

    if not checker.is_exists_the_word(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="word"), _fname)
        return False

    if not _edit_the_file(editor, ppath.get_word_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target="word"), _fname)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target="word"))
    return True


# Private Functions
def _edit_the_file(editor: str, fname: str) -> bool:
    assert isinstance(editor, str)
    assert isinstance(fname, str)

    proc = subprocess.run([editor, fname])
    if proc.returncode != 0:
        logger.error("Subprocess Error!: %s", proc.returncode)
        return False
    return True


def _get_editor() -> str:
    proj_data = assertion.is_dict(read_file_as_yaml(ppath.get_project_path()))
    data = proj_data['storybuilder']
    editor = data['editor'] if data['editor'] else DEFAULT_EDITOR
    return editor


def _get_target_filename(fname: str, msg: str, targets: list) -> str:
    assert isinstance(msg, str)
    assert isinstance(targets, list)

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
