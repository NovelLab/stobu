"""Add and Delete module for storybuilder project."""


# Official Libraries
import argparse
import os
import shutil
from typing import Callable


# My Modules
from stobu.commands.projecteditor import edit_the_chapter, edit_the_episode, edit_the_scene, edit_the_note
from stobu.commands.projecteditor import edit_the_person, edit_the_stage, edit_the_item, edit_the_word
from stobu.commands.projecteditor import edit_the_plan, edit_the_outline, edit_the_event
from stobu.templatecreator import TemplateCreator
from stobu import todomanager as todom
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import write_file
from stobu.util.filepath import get_input_filename
from stobu.util.log import logger


__all__ = (
        'switch_command_to_add',
        'switch_command_to_copy',
        'switch_command_to_delete',
        'switch_command_to_rename',
        )


# Define Constants
INPUT_TARGET_FILENAME_MESSAGE = "Enter {target} file name: "
"""str: message to get a new file name."""

INPUT_TARGET_FILENAME_WITH_LIST_MESSAGE = "{target_list}\nEnter {target} file name: "
"""str: message to get the deleting file name."""

START_ADD_PROCESS_MESSAGE = "Adding a new {target} file..."
"""str: message to start adding process."""

FINISH_ADD_PROCESS_MESSAGE = "...Succeeded add new {target}."
"""str: message to finish the adding process as successfull."""

START_COPY_PROCESS_MESSAGE = "Copying the {target} file..."
"""str: message to start copying process."""

FINISH_COPY_PROCESS_MESSAGE = "...Succeeded copy the {target} file."
"""str: message to finish the copying process as successfull."""

START_DELETE_PROCESS_MESSAGE = "Deleting the {target} file..."
"""str: message to start deleting process."""

FINISH_DELETE_PROCESS_MESSAGE = "...Succeeded delete the {target}."
"""str: message to finish the deleting process as successfull."""

START_RENAME_PROCESS_MESSAGE = "Renaming the {target} file..."
"""str: message to start renaming process."""

FINISH_RENAME_PROCESS_MESSAGE = "...Succeeded rename the {target}."
"""str: message to finish the renaming process."""

ERR_MESSAGE_DUPLICATED = "Already the {target} file exists!: %s"
"""str: error message when the file already exists."""

ERR_MESSAGE_INVALID_FILENAME = "Invalid the file name!: %s"
"""str: error message when the file name is invalid."""

ERR_MESSAGE_MISSING_FILE = "Not Found the {target} file!: %s"
"""str: error message when the file not found."""

ERR_MESSAGE_CANNOT_CREATE = "Failed to create the {target} file!: %s"
"""str: error message when the file cannot create."""

ERR_MESSAGE_CANNOT_COPY = "Failed to copy the {target} file!: %s"
"""str: error message when the file cannot copy."""

ERR_MESSAGE_CANNOT_REMOVE = "Failed to remove the {target} file!: %s"
"""str: error message when the file cannot remove."""

ERR_MESSAGE_CANNOT_RENAME = "Failed to rename the {target} file!: %s > %s"
"""str: error message when the file cannot rename."""


# Main Function
def switch_command_to_add(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('a', 'add')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = add_new_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = add_new_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = add_new_scene(cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = add_new_note(cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = add_new_person(cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = add_new_stage(cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = add_new_item(cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = add_new_word(cmdargs.arg1)
    elif cmdargs.arg0 in ('d', 'todo'):
        is_succeeded = todom.add_todo(cmdargs.arg1)
    elif cmdargs.arg0 in ('l', 'plan'):
        is_succeeded = add_new_plan(cmdargs.arg1)
    elif cmdargs.arg0 in ('o', 'outline'):
        is_succeeded = add_new_outline(cmdargs.arg1)
    elif cmdargs.arg0 in ('v', 'event'):
        is_succeeded = add_new_event(cmdargs.arg1)
    else:
        logger.error("Unknown add command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command add!")
        return False

    logger.debug("...Succeeded command add.")
    return True


def switch_command_to_copy(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('c', 'copy')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = copy_the_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = copy_the_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = copy_the_scene(cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = copy_the_note(cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = copy_the_person(cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = copy_the_stage(cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = copy_the_item(cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = copy_the_word(cmdargs.arg1)
    elif cmdargs.arg0 in ('l', 'plan'):
        is_succeeded = copy_the_plan(cmdargs.arg1)
    elif cmdargs.arg0 in ('o', 'outline'):
        is_succeeded = copy_the_outline(cmdargs.arg1)
    elif cmdargs.arg0 in ('v', 'event'):
        is_succeeded = copy_the_event(cmdargs.arg1)
    else:
        logger.error("Unknown delete command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command copy!")
        return False

    logger.debug("...Succeeded command copy.")
    return True


def switch_command_to_delete(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('d', 'delete')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = delete_the_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = delete_the_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = delete_the_scene(cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = delete_the_note(cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = delete_the_person(cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = delete_the_stage(cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = delete_the_item(cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = delete_the_word(cmdargs.arg1)
    elif cmdargs.arg0 in ('l', 'plan'):
        is_succeeded = delete_the_plan(cmdargs.arg1)
    elif cmdargs.arg0 in ('o', 'outline'):
        is_succeeded = delete_the_outline(cmdargs.arg1)
    elif cmdargs.arg0 in ('v', 'event'):
        is_succeeded = delete_the_event(cmdargs.arg1)
    else:
        logger.error("Unknown delete command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command delete!")
        return False

    logger.debug("...Succeeded command delete.")
    return True


def switch_command_to_rename(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('r', 'rename')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = rename_the_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = rename_the_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = rename_the_scene(cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = rename_the_note(cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = rename_the_person(cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = rename_the_stage(cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = rename_the_item(cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = rename_the_word(cmdargs.arg1)
    elif cmdargs.arg0 in ('l', 'plan'):
        is_succeeded = rename_the_plan(cmdargs.arg1)
    elif cmdargs.arg0 in ('o', 'outline'):
        is_succeeded = rename_the_outline(cmdargs.arg1)
    elif cmdargs.arg0 in ('v', 'event'):
        is_succeeded = rename_the_event(cmdargs.arg1)
    else:
        logger.error("Unknown delete command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command rename!")
        return False

    logger.debug("...Succeeded command rename.")
    return True


# Functions
# - Add
def add_new_chapter(fname: str) -> bool:
    return _add_new_file('chapter', fname, checker.is_exists_the_chapter,
            ppath.get_chapter_path,
            TemplateCreator.get_instance().get_chapter_template,
            edit_the_chapter)


def add_new_episode(fname: str) -> bool:
    return _add_new_file('episode', fname, checker.is_exists_the_episode,
            ppath.get_episode_path,
            TemplateCreator.get_instance().get_episode_template,
            edit_the_episode)


def add_new_event(fname: str) -> bool:
    return _add_new_file('event', fname, checker.is_exists_the_event,
            ppath.get_event_path,
            TemplateCreator.get_instance().get_event_template,
            edit_the_event)


def add_new_item(fname: str) -> bool:
    return _add_new_file('item', fname, checker.is_exists_the_item,
            ppath.get_item_path,
            TemplateCreator.get_instance().get_item_template,
            edit_the_item)


def add_new_note(fname: str) -> bool:
    return _add_new_file('note', fname, checker.is_exists_the_note,
            ppath.get_note_path,
            TemplateCreator.get_instance().get_note_template,
            edit_the_note)


def add_new_outline(fname: str) -> bool:
    return _add_new_file('outline', fname, checker.is_exists_the_outline,
            ppath.get_outline_path,
            TemplateCreator.get_instance().get_outline_template,
            edit_the_outline)


def add_new_person(fname: str) -> bool:
    return _add_new_file('person', fname, checker.is_exists_the_person,
            ppath.get_person_path,
            TemplateCreator.get_instance().get_person_template,
            edit_the_person)


def add_new_plan(fname: str) -> bool:
    return _add_new_file('plan', fname, checker.is_exists_the_plan,
            ppath.get_plan_path,
            TemplateCreator.get_instance().get_plan_template,
            edit_the_plan)


def add_new_scene(fname: str) -> bool:
    return _add_new_file('scene', fname, checker.is_exists_the_scene,
            ppath.get_scene_path,
            TemplateCreator.get_instance().get_scene_template,
            edit_the_scene)


def add_new_stage(fname: str) -> bool:
    return _add_new_file('stage', fname, checker.is_exists_the_stage,
            ppath.get_stage_path,
            TemplateCreator.get_instance().get_stage_template,
            edit_the_stage)


def add_new_word(fname: str) -> bool:
    return _add_new_file('word', fname, checker.is_exists_the_word,
            ppath.get_word_path,
            TemplateCreator.get_instance().get_word_template,
            edit_the_word)


# - Copy
def copy_the_chapter(fname: str) -> bool:
    return _copy_the_file('chapter', fname, checker.is_exists_the_chapter,
            ppath.get_chapter_file_names, ppath.get_chapter_path)


def copy_the_episode(fname: str) -> bool:
    return _copy_the_file('episode', fname, checker.is_exists_the_episode,
            ppath.get_episode_file_names, ppath.get_episode_path)


def copy_the_event(fname: str) -> bool:
    return _copy_the_file('event', fname, checker.is_exists_the_event,
            ppath.get_event_file_names, ppath.get_event_path)


def copy_the_scene(fname: str) -> bool:
    return _copy_the_file('scene', fname, checker.is_exists_the_scene,
            ppath.get_scene_file_names, ppath.get_scene_path)


def copy_the_note(fname: str) -> bool:
    return _copy_the_file('note', fname, checker.is_exists_the_note,
            ppath.get_note_file_names, ppath.get_note_path)


def copy_the_outline(fname: str) -> bool:
    return _copy_the_file('outline', fname, checker.is_exists_the_outline,
            ppath.get_outline_file_names, ppath.get_outline_path)


def copy_the_person(fname: str) -> bool:
    return _copy_the_file('person', fname, checker.is_exists_the_person,
            ppath.get_person_file_names, ppath.get_person_path)


def copy_the_plan(fname: str) -> bool:
    return _copy_the_file('plan', fname, checker.is_exists_the_plan,
            ppath.get_plan_file_names, ppath.get_plan_path)


def copy_the_stage(fname: str) -> bool:
    return _copy_the_file('stage', fname, checker.is_exists_the_stage,
            ppath.get_stage_file_names, ppath.get_stage_path)


def copy_the_item(fname: str) -> bool:
    return _copy_the_file('item', fname, checker.is_exists_the_item,
            ppath.get_item_file_names, ppath.get_item_path)


def copy_the_word(fname: str) -> bool:
    return _copy_the_file('word', fname, checker.is_exists_the_word,
            ppath.get_word_file_names, ppath.get_word_path)


# - Delete
def delete_the_chapter(fname: str) -> bool:
    return _delete_the_file('chapter', fname, checker.is_exists_the_chapter,
            ppath.get_chapter_file_names, ppath.get_chapter_path)


def delete_the_episode(fname: str) -> bool:
    return _delete_the_file('episode', fname, checker.is_exists_the_episode,
            ppath.get_episode_file_names, ppath.get_episode_path)


def delete_the_event(fname: str) -> bool:
    return _delete_the_file('event', fname, checker.is_exists_the_event,
            ppath.get_event_file_names, ppath.get_event_path)


def delete_the_scene(fname: str) -> bool:
    return _delete_the_file('scene', fname, checker.is_exists_the_scene,
            ppath.get_scene_file_names, ppath.get_scene_path)


def delete_the_note(fname: str) -> bool:
    return _delete_the_file('note', fname, checker.is_exists_the_note,
            ppath.get_note_file_names, ppath.get_note_path)


def delete_the_outline(fname: str) -> bool:
    return _delete_the_file('outline', fname, checker.is_exists_the_outline,
            ppath.get_outline_file_names, ppath.get_outline_path)


def delete_the_person(fname: str) -> bool:
    return _delete_the_file('person', fname, checker.is_exists_the_person,
            ppath.get_person_file_names, ppath.get_person_path)


def delete_the_plan(fname: str) -> bool:
    return _delete_the_file('plan', fname, checker.is_exists_the_plan,
            ppath.get_plan_file_names, ppath.get_plan_path)


def delete_the_stage(fname: str) -> bool:
    return _delete_the_file('stage', fname, checker.is_exists_the_stage,
            ppath.get_stage_file_names, ppath.get_stage_path)


def delete_the_item(fname: str) -> bool:
    return _delete_the_file('item', fname, checker.is_exists_the_item,
            ppath.get_item_file_names, ppath.get_item_path)


def delete_the_word(fname: str) -> bool:
    return _delete_the_file('word', fname, checker.is_exists_the_word,
            ppath.get_word_file_names, ppath.get_word_path)


# - Rename
def rename_the_chapter(fname: str) -> bool:
    return _rename_the_file('chapter', fname, checker.is_exists_the_chapter,
            ppath.get_chapter_file_names, ppath.get_chapter_path)


def rename_the_episode(fname: str) -> bool:
    return _rename_the_file('episode', fname, checker.is_exists_the_episode,
            ppath.get_episode_file_names, ppath.get_episode_path)


def rename_the_event(fname: str) -> bool:
    return _rename_the_file('event', fname, checker.is_exists_the_event,
            ppath.get_event_file_names, ppath.get_event_path)


def rename_the_scene(fname: str) -> bool:
    return _rename_the_file('scene', fname, checker.is_exists_the_scene,
            ppath.get_scene_file_names, ppath.get_scene_path)


def rename_the_note(fname: str) -> bool:
    return _rename_the_file('note', fname, checker.is_exists_the_note,
            ppath.get_note_file_names, ppath.get_note_path)


def rename_the_outline(fname: str) -> bool:
    return _rename_the_file('outline', fname, checker.is_exists_the_outline,
            ppath.get_outline_file_names, ppath.get_outline_path)


def rename_the_person(fname: str) -> bool:
    return _rename_the_file('person', fname, checker.is_exists_the_person,
            ppath.get_person_file_names, ppath.get_person_path)


def rename_the_plan(fname: str) -> bool:
    return _rename_the_file('plan', fname, checker.is_exists_the_plan,
            ppath.get_plan_file_names, ppath.get_plan_path)


def rename_the_stage(fname: str) -> bool:
    return _rename_the_file('stage', fname, checker.is_exists_the_stage,
            ppath.get_stage_file_names, ppath.get_stage_path)


def rename_the_item(fname: str) -> bool:
    return _rename_the_file('item', fname, checker.is_exists_the_item,
            ppath.get_item_file_names, ppath.get_item_path)


def rename_the_word(fname: str) -> bool:
    return _rename_the_file('word', fname, checker.is_exists_the_word,
            ppath.get_word_file_names, ppath.get_word_path)


# Private Functions
def _add_new_file(title: str, fname: str, check_method: Callable,
        path_method: Callable, gettemp_method: Callable, edit_method) -> bool:
    assert isinstance(title, str)
    assert isinstance(fname, str) if fname else True
    assert callable(check_method)
    assert callable(path_method)
    assert callable(gettemp_method)
    assert callable(edit_method)
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target=title))

    _fname = _get_new_filename(fname, f"new {title}")

    if checker.is_invalid_filename(_fname):
        logger.error(ERR_MESSAGE_INVALID_FILENAME, _fname)
        return False

    if check_method(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target=title), _fname)
        return False

    template_data = gettemp_method()
    if not write_file(path_method(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target=title), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target=title))

    return edit_method(_fname)


def _copyfile(fname: str, newname: str) -> bool:
    if not fname or not newname:
        return False
    else:
        shutil.copyfile(fname, newname)
        return True


def _copy_the_file(title: str, fname: str, check_method: Callable,
        list_method: Callable, path_method: Callable) -> bool:
    assert isinstance(title, str)
    assert isinstance(fname, str) if fname else True
    assert callable(check_method)
    assert callable(list_method)
    assert callable(path_method)
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target=title))

    _fname = _get_target_filename(fname, f"copying {title}", list_method())

    if checker.is_invalid_filename(_fname):
        logger.error(ERR_MESSAGE_INVALID_FILENAME, _fname)
        return False

    if not check_method(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target=title), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(path_method(_fname), path_method(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target=title), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target=title))
    return True


def _delete_the_file(title: str, fname: str, check_method: Callable,
        list_method: Callable, path_method: Callable) -> bool:
    assert isinstance(title, str)
    assert isinstance(fname, str) if fname else True
    assert callable(check_method)
    assert callable(list_method)
    assert callable(path_method)
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target=title))

    _fname = _get_target_filename(fname, f"deleting {title}", list_method())

    if checker.is_invalid_filename(_fname):
        logger.error(ERR_MESSAGE_INVALID_FILENAME, _fname)
        return False

    if not check_method(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target=title), _fname)
        return False

    if not _move_to_trash(path_method(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target=title), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target=title))
    return True


def _get_new_filename(fname: str, msg: str) -> str:
    assert isinstance(msg, str)

    return assertion.is_str(fname) if fname else get_input_filename(
            INPUT_TARGET_FILENAME_MESSAGE.format(target=msg))


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


def _move_to_trash(fname: str) -> bool:
    if not fname:
        return False
    else:
        shutil.move(fname, ppath.get_trash_dir_path())
        return True


def _renamefile(fname: str, newfname: str) -> bool:
    assert isinstance(fname, str)
    assert isinstance(newfname, str)

    if newfname:
        os.rename(fname, newfname)
        return True
    else:
        return False


def _rename_the_file(title: str, fname: str, check_method: Callable,
        list_method: Callable, path_method: Callable) -> bool:
    assert isinstance(title, str)
    assert isinstance(fname, str) if fname else True
    assert callable(check_method)
    assert callable(list_method)
    assert callable(path_method)
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target=title))

    _fname = _get_target_filename(fname, f"renaming {title}", list_method())

    if checker.is_invalid_filename(_fname):
        logger.error(ERR_MESSAGE_INVALID_FILENAME, _fname)
        return False

    if not check_method(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target=title), _fname)
        return False

    _new = _get_new_filename("", f"new {title}")
    if check_method(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target=title), _new)
        return False

    if not _renamefile(path_method(_fname), path_method(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target=title), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target=title))
    return True


