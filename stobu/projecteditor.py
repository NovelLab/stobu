"""Edit module for storybuilder project."""


# Official Libraries
import argparse
import subprocess
from typing import Callable


# My Modules
from stobu.dataconverter import conv_to_dumpdata_of_yaml
from stobu.settings import DEFAULT_EDITOR, YAML_EXT, MARKDOWN_EXT
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import read_file_as_auto, write_file
from stobu.util.filepath import get_input_filename
from stobu.util.log import logger


__all__ = (
        'edit_the_book', 'edit_the_order',
        'edit_the_chapter', 'edit_the_episode', 'edit_the_scene', 'edit_the_note',
        'edit_the_person', 'edit_the_stage', 'edit_the_item', 'edit_the_word',
        'edit_the_plan', 'edit_the_outline', 'edit_the_event',
        'edit_todo',
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
    elif cmdargs.arg0 in ('d', 'todo'):
        is_succeeded = edit_todo()
    elif cmdargs.arg0 in ('l', 'plan'):
        is_succeeded = edit_the_plan(cmdargs.arg1)
    elif cmdargs.arg0 in ('o', 'outline'):
        is_succeeded = edit_the_outline(cmdargs.arg1)
    elif cmdargs.arg0 in ('v', 'event'):
        is_succeeded = edit_the_event(cmdargs.arg1)
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
    proj_data = read_file_as_auto(ppath.get_project_path())
    proj_data['storybuilder']['editor'] = editor

    if not write_file(ppath.get_project_path(), conv_to_dumpdata_of_yaml(proj_data)):
        logger.error("...Failed to set the editor!: %s", editor)
        return False

    return True


# Functions
def edit_the_book() -> bool:
    return _edit_the_file('book', ppath.get_book_path(),
            checker.exists_book_file,
            False, None, None)


def edit_the_chapter(fname: str) -> bool:
    return _edit_the_file('chapter', fname,
            checker.is_exists_the_chapter,
            True,
            ppath.get_chapter_file_names, ppath.get_chapter_path)


def edit_the_episode(fname: str) -> bool:
    return _edit_the_file('episode', fname,
            checker.is_exists_the_episode,
            True,
            ppath.get_episode_file_names, ppath.get_episode_path)


def edit_the_event(fname: str) -> bool:
    return _edit_the_file('event', fname,
            checker.is_exists_the_event,
            True,
            ppath.get_event_file_names, ppath.get_event_path)


def edit_the_item(fname: str) -> bool:
    return _edit_the_file('item', fname,
            checker.is_exists_the_item,
            True,
            ppath.get_item_file_names, ppath.get_item_path)


def edit_the_note(fname: str) -> bool:
    return _edit_the_file('note', fname,
            checker.is_exists_the_note,
            True,
            ppath.get_note_file_names, ppath.get_note_path)


def edit_the_order() -> bool:
    return _edit_the_file('order', ppath.get_order_path(),
            checker.exists_order_file,
            False, None, None)


def edit_the_outline(fname: str) -> bool:
    return _edit_the_file('outline', fname,
            checker.is_exists_the_outline,
            True,
            ppath.get_outline_file_names, ppath.get_outline_path)


def edit_the_person(fname: str) -> bool:
    return _edit_the_file('person', fname,
            checker.is_exists_the_person,
            True,
            ppath.get_person_file_names, ppath.get_person_path)


def edit_the_plan(fname: str) -> bool:
    return _edit_the_file('plan', fname,
            checker.is_exists_the_plan,
            True,
            ppath.get_plan_file_names, ppath.get_plan_path)


def edit_the_scene(fname: str) -> bool:
    return _edit_the_file('scene', fname,
            checker.is_exists_the_scene,
            True,
            ppath.get_scene_file_names, ppath.get_scene_path)


def edit_the_stage(fname: str) -> bool:
    return _edit_the_file('stage', fname,
            checker.is_exists_the_stage,
            True,
            ppath.get_stage_file_names, ppath.get_stage_path)


def edit_the_word(fname: str) -> bool:
    return _edit_the_file('word', fname,
            checker.is_exists_the_word,
            True,
            ppath.get_word_file_names, ppath.get_word_path)


def edit_todo() -> bool:
    return _edit_the_file('todo', ppath.get_todo_path(),
            checker.exists_todo_file,
            False,
            None, None)


# Private Functions
def _edit_the_file(title: str, fname: str,
        check_method: Callable,
        with_list: bool,
        list_method: Callable,
        path_method: Callable) -> bool:
    assert isinstance(title, str)
    assert isinstance(fname, str) if fname else True
    assert callable(check_method)
    assert isinstance(with_list, bool)
    if with_list:
        assert callable(path_method)
        assert callable(list_method)
    logger.debug(START_EDIT_PROCESS_MESSAGE.format(target=title))

    _fname = fname
    if with_list:
        filenames = list_method()
        _fname = _get_target_filename(fname, f"editing {title}", filenames)
    else:
        _fname = fname

    if with_list:
        if not check_method(_fname):
            logger.error(ERR_MESSAGE_MISSING_FILE.format(target=title), _fname)
            return False
    elif not check_method():
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target=title), _fname)
        return False

    path = path_method(_fname) if with_list else _fname
    if not _run_subprocess_to_edit_file(path):
        logger.error(ERR_MESSAGE_CANNOT_EDIT.format(target=title), path)
        return False

    logger.debug(FINISH_EDIT_PROCESS_MESSAGE.format(target=title))
    return True


def _get_editor() -> str:
    proj_data = assertion.is_dict(read_file_as_auto(ppath.get_project_path()))
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


def _run_subprocess_to_edit_file(fname: str) -> bool:
    assert isinstance(fname, str)

    editor = assertion.is_str(_get_editor())
    proc = subprocess.run([editor, fname])
    if proc.returncode != 0:
        logger.error("Subprocess Error!: %s", proc.returncode)
        return False
    return True
