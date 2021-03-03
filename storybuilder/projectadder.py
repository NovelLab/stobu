"""Add and Delete module for storybuilder project."""


# Official Libraries
import argparse
import os
import shutil


# My Modules
import storybuilder.projectfilechecker as checker
import storybuilder.projectpathmanager as ppath
from storybuilder.projecteditor import edit_the_chapter, edit_the_episode, edit_the_scene, edit_the_note
from storybuilder.projecteditor import edit_the_person, edit_the_stage, edit_the_item, edit_the_word
from storybuilder.templatecreator import TemplateCreator
from storybuilder.util import assertion
from storybuilder.util.fileio import write_file
from storybuilder.util.filepath import get_input_filename
from storybuilder.util.log import logger


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
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="chapter"))

    _fname = _get_new_filename(fname, "new chapter")

    if checker.is_exists_the_chapter(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="chapter"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_chapter_template()
    if not write_file(ppath.get_chapter_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="chapter"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="chapter"))

    return edit_the_chapter(_fname)


def add_new_episode(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="episode"))

    _fname = _get_new_filename(fname, "new episode")

    if checker.is_exists_the_episode(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="episode"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_episode_template()
    if not write_file(ppath.get_episode_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="episode"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="episode"))

    return edit_the_episode(_fname)


def add_new_item(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="item"))

    _fname = _get_new_filename(fname, "new item")

    if checker.is_exists_the_item(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="item"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_item_template()
    if not write_file(ppath.get_item_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="item"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="item"))

    return edit_the_item(_fname)


def add_new_note(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="note"))

    _fname = _get_new_filename(fname, "new note")

    if checker.is_exists_the_note(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="note"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_note_template()
    if not write_file(ppath.get_note_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="note"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="note"))

    return edit_the_note(_fname)


def add_new_person(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="person"))

    _fname = _get_new_filename(fname, "new person")

    if checker.is_exists_the_person(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="person"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_person_template()
    if not write_file(ppath.get_person_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="person"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="person"))

    return edit_the_person(_fname)


def add_new_scene(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="scene"))

    _fname = _get_new_filename(fname, "new scene")

    if checker.is_exists_the_scene(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="scene"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_scene_template()
    if not write_file(ppath.get_scene_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="scene"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="scene"))

    return edit_the_scene(_fname)


def add_new_stage(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="stage"))

    _fname = _get_new_filename(fname, "new stage")

    if checker.is_exists_the_stage(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="stage"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_stage_template()
    if not write_file(ppath.get_stage_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="stage"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="stage"))

    return edit_the_stage(_fname)


def add_new_word(fname: str) -> bool:
    logger.debug(START_ADD_PROCESS_MESSAGE.format(target="word"))

    _fname = _get_new_filename(fname, "new word")

    if checker.is_exists_the_word(_fname):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="word"), _fname)
        return False

    template_data = TemplateCreator.get_instance().get_word_template()
    if not write_file(ppath.get_word_path(_fname), template_data):
        logger.error(ERR_MESSAGE_CANNOT_CREATE.format(target="word"), _fname)
        return False

    logger.debug(FINISH_ADD_PROCESS_MESSAGE.format(target="word"))

    return edit_the_word(_fname)


# - Copy
def copy_the_chapter(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="chapter"))

    chapters = ppath.get_chapter_file_names()
    _fname = _get_target_filename(fname, "copying chapter", chapters)

    if not checker.is_exists_the_chapter(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_chapter_path(_fname), ppath.get_chapter_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="chapter"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="chapter"))
    return True


def copy_the_episode(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="episode"))

    episodes = ppath.get_episode_file_names()
    _fname = _get_target_filename(fname, "copying episode", episodes)

    if not checker.is_exists_the_episode(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_episode_path(_fname), ppath.get_episode_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="episode"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="episode"))
    return True


def copy_the_scene(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="scene"))

    scenes = ppath.get_scene_file_names()
    _fname = _get_target_filename(fname, "copying scene", scenes)

    if not checker.is_exists_the_scene(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_scene_path(_fname), ppath.get_scene_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="scene"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="scene"))
    return True


def copy_the_note(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="note"))

    notes = ppath.get_note_file_names()
    _fname = _get_target_filename(fname, "copying note", notes)

    if not checker.is_exists_the_note(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="note"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_note_path(_fname), ppath.get_note_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="note"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="note"))
    return True


def copy_the_person(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="person"))

    persons = ppath.get_person_file_names()
    _fname = _get_target_filename(fname, "copying person", persons)

    if not checker.is_exists_the_person(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="person"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_person_path(_fname), ppath.get_person_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="person"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="person"))
    return True


def copy_the_stage(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="stage"))

    stages = ppath.get_stage_file_names()
    _fname = _get_target_filename(fname, "copying stage", stages)

    if not checker.is_exists_the_stage(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="stage"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_stage_path(_fname), ppath.get_stage_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="stage"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="stage"))
    return True


def copy_the_item(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="item"))

    items = ppath.get_item_file_names()
    _fname = _get_target_filename(fname, "copying item", items)

    if not checker.is_exists_the_item(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="item"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_item_path(_fname), ppath.get_item_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="item"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="item"))
    return True


def copy_the_word(fname: str) -> bool:
    logger.debug(START_COPY_PROCESS_MESSAGE.format(target="word"))

    words = ppath.get_word_file_names()
    _fname = _get_target_filename(fname, "copying word", words)

    if not checker.is_exists_the_word(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="word"), _fname)
        return False

    _new = f"{_fname}_"
    if not _copyfile(ppath.get_word_path(_fname), ppath.get_word_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_COPY.format(target="word"), _fname)
        return False

    logger.debug(FINISH_COPY_PROCESS_MESSAGE.format(target="word"))
    return True


# - Delete
def delete_the_chapter(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="chapter"))

    chapters = ppath.get_chapter_file_names()
    _fname = _get_target_filename(fname, "deleting chapter", chapters)

    if not checker.is_exists_the_chapter(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    if not _move_to_trash(ppath.get_chapter_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="chapter"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="chapter"))
    return True


def delete_the_episode(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="episode"))

    episodes = ppath.get_episode_file_names()
    _fname = _get_target_filename(fname, "deleting episode", episodes)

    if not checker.is_exists_the_episode(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    if not _move_to_trash(ppath.get_episode_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="episode"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="episode"))
    return True


def delete_the_scene(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="scene"))

    scenes = ppath.get_scene_file_names()
    _fname = _get_target_filename(fname, "deleting scene", scenes)

    if not checker.is_exists_the_scene(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    if not _move_to_trash(ppath.get_scene_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="scene"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="scene"))
    return True


def delete_the_note(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="note"))

    notes = ppath.get_note_file_names()
    _fname = _get_target_filename(fname, "deleting note", notes)

    if not checker.is_exists_the_note(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="note"), _fname)
        return False

    if not _move_to_trash(ppath.get_note_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="note"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="note"))
    return True


def delete_the_person(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="person"))

    persons = ppath.get_person_file_names()
    _fname = _get_target_filename(fname, "deleting person", persons)

    if not checker.is_exists_the_person(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="person"), _fname)
        return False

    if not _move_to_trash(ppath.get_person_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="person"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="person"))
    return True


def delete_the_stage(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="stage"))

    stages = ppath.get_stage_file_names()
    _fname = _get_target_filename(fname, "deleting stage", stages)

    if not checker.is_exists_the_stage(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="stage"), _fname)
        return False

    if not _move_to_trash(ppath.get_stage_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="stage"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="stage"))
    return True


def delete_the_item(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="item"))

    items = ppath.get_item_file_names()
    _fname = _get_target_filename(fname, "deleting item", items)

    if not checker.is_exists_the_item(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="item"), _fname)
        return False

    if not _move_to_trash(ppath.get_item_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="item"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="item"))
    return True


def delete_the_word(fname: str) -> bool:
    logger.debug(START_DELETE_PROCESS_MESSAGE.format(target="word"))

    words = ppath.get_word_file_names()
    _fname = _get_target_filename(fname, "deleting word", words)

    if not checker.is_exists_the_word(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="word"), _fname)
        return False

    if not _move_to_trash(ppath.get_word_path(_fname)):
        logger.error(ERR_MESSAGE_CANNOT_REMOVE.format(target="word"), _fname)
        return False

    logger.debug(FINISH_DELETE_PROCESS_MESSAGE.format(target="word"))
    return True


# - Rename
def rename_the_chapter(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="chapter"))

    chapters = ppath.get_chapter_file_names()
    _fname = _get_target_filename(fname, "renaming chapter", chapters)

    if not checker.is_exists_the_chapter(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    _new = _get_new_filename("", "new chapter")
    if checker.is_exists_the_chapter(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="chapter"), _new)
        return False

    if not _renamefile(ppath.get_chapter_path(_fname), ppath.get_chapter_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="chapter"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="chapter"))
    return True


def rename_the_episode(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="episode"))

    episodes = ppath.get_episode_file_names()
    _fname = _get_target_filename(fname, "renaming episode", episodes)

    if not checker.is_exists_the_episode(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    _new = _get_new_filename("", "new episode")
    if checker.is_exists_the_episode(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="episode"), _new)
        return False

    if not _renamefile(ppath.get_episode_path(_fname), ppath.get_episode_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="episode"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="episode"))
    return True


def rename_the_scene(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="scene"))

    scenes = ppath.get_scene_file_names()
    _fname = _get_target_filename(fname, "renaming scene", scenes)

    if not checker.is_exists_the_scene(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    _new = _get_new_filename("", "new scene")
    if checker.is_exists_the_scene(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="scene"), _new)
        return False

    if not _renamefile(ppath.get_scene_path(_fname), ppath.get_scene_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="scene"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="scene"))
    return True


def rename_the_note(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="note"))

    notes = ppath.get_note_file_names()
    _fname = _get_target_filename(fname, "renaming note", notes)

    if not checker.is_exists_the_note(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="note"), _fname)
        return False

    _new = _get_new_filename("", "new note")
    if checker.is_exists_the_note(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="note"), _new)
        return False

    if not _renamefile(ppath.get_note_path(_fname), ppath.get_note_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="note"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="note"))
    return True


def rename_the_person(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="person"))

    persons = ppath.get_person_file_names()
    _fname = _get_target_filename(fname, "renaming person", persons)

    if not checker.is_exists_the_person(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="person"), _fname)
        return False

    _new = _get_new_filename("", "new person")
    if checker.is_exists_the_person(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="person"), _new)
        return False

    if not _renamefile(ppath.get_person_path(_fname), ppath.get_person_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="person"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="person"))
    return True


def rename_the_stage(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="stage"))

    stages = ppath.get_stage_file_names()
    _fname = _get_target_filename(fname, "renaming stage", stages)

    if not checker.is_exists_the_stage(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="stage"), _fname)
        return False

    _new = _get_new_filename("", "new stage")
    if checker.is_exists_the_stage(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="stage"), _new)
        return False

    if not _renamefile(ppath.get_stage_path(_fname), ppath.get_stage_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="stage"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="stage"))
    return True


def rename_the_item(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="item"))

    items = ppath.get_item_file_names()
    _fname = _get_target_filename(fname, "renaming item", items)

    if not checker.is_exists_the_item(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="item"), _fname)
        return False

    _new = _get_new_filename("", "new item")
    if checker.is_exists_the_item(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="item"), _new)
        return False

    if not _renamefile(ppath.get_item_path(_fname), ppath.get_item_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="item"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="item"))
    return True


def rename_the_word(fname: str) -> bool:
    logger.debug(START_RENAME_PROCESS_MESSAGE.format(target="word"))

    words = ppath.get_word_file_names()
    _fname = _get_target_filename(fname, "renaming word", words)

    if not checker.is_exists_the_word(_fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="word"), _fname)
        return False

    _new = _get_new_filename("", "new word")
    if checker.is_exists_the_word(_new):
        logger.error(ERR_MESSAGE_DUPLICATED.format(target="word"), _new)
        return False

    if not _renamefile(ppath.get_word_path(_fname), ppath.get_word_path(_new)):
        logger.error(ERR_MESSAGE_CANNOT_RENAME.format(target="word"), _fname, _new)
        return False

    logger.debug(FINISH_RENAME_PROCESS_MESSAGE.format(target="word"))
    return True


# Private Functions
def _copyfile(fname: str, newname: str) -> bool:
    shutil.copyfile(fname, newname)
    return True


def _get_new_filename(fname: str, msg: str) -> str:
    return assertion.is_str(fname) if fname else get_input_filename(
            INPUT_TARGET_FILENAME_MESSAGE.format(target=msg))


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


def _move_to_trash(fname: str) -> bool:
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
