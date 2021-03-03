"""View module for storybuilder project."""


# Official Libraries
import argparse


# My Modules
from storybuilder.dataconverter import conv_to_dumpdata_of_yaml
import storybuilder.projectpathmanager as ppath
from storybuilder.util.fileio import read_file_as_yaml
from storybuilder.util.filepath import basename_of
from storybuilder.util.log import logger


__all__ = (
        'switch_command_to_list',
        )


# Define Constants
INPUT_TARGET_FILENAME_WITH_LIST_MESSAGE = "{target_list}\nEnter {target} file name: "
"""str: message to get the deleting file name."""

START_LIST_PROCESS_MESSAGE = "Editing the {target} file..."
"""str: message to start editing process."""

FINISH_LIST_PROCESS_MESSAGE = "...Succeeded edit {target} file."
"""str: message to finish the editing process as successfull."""

ERR_MESSAGE_CANNOT_SHOW_LIST = "Cannot show the {target} list!"
"""str: error message when cannot show the list."""


# Main Function
def switch_command_to_list(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('l', 'list')

    is_succeeded = False

    if cmdargs.arg0 in ('o', 'order'):
        is_succeeded = show_list_of_orders()
    elif cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = show_list_of_chapters()
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = show_list_of_episodes()
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = show_list_of_scenes()
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = show_list_of_notes()
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = show_list_of_persons()
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = show_list_of_stages()
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = show_list_of_items()
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = show_list_of_words()
    else:
        logger.error("Unknown add command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command show list.")
        return False

    logger.debug("...Succeeded command show list.")
    return True


# Functions
def show_list_of_chapters() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="chapter"))

    if not _show_list("> Chapter list:", ppath.get_chapter_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="chapter"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="chapter"))
    return True


def show_list_of_episodes() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="episode"))

    if not _show_list("> Episode list:", ppath.get_episode_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="episode"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="episode"))
    return True


def show_list_of_items() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="item"))

    if not _show_list("> Item list:", ppath.get_item_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="item"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="item"))
    return True


def show_list_of_notes() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="note"))

    if not _show_list("> Note list:", ppath.get_note_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="note"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="note"))
    return True


def show_list_of_orders() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="order"))

    order_data = read_file_as_yaml(ppath.get_order_path())

    # NOTE: format を考える
    print("> Order data:")
    print(conv_to_dumpdata_of_yaml(order_data))

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="order"))
    return True


def show_list_of_persons() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="person"))

    if not _show_list("> Person list:", ppath.get_person_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="person"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="person"))
    return True


def show_list_of_scenes() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="scene"))

    if not _show_list("> Scene list:", ppath.get_scene_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="scene"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="scene"))
    return True


def show_list_of_stages() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="stage"))

    if not _show_list("> Stage list:", ppath.get_stage_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="stage"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="stage"))
    return True


def show_list_of_words() -> bool:
    logger.debug(START_LIST_PROCESS_MESSAGE.format(target="word"))

    if not _show_list("> Word list:", ppath.get_word_file_names()):
        logger.error(ERR_MESSAGE_CANNOT_SHOW_LIST.format(target="word"))
        return False

    logger.debug(FINISH_LIST_PROCESS_MESSAGE.format(target="word"))
    return True


# Private Functions
def _show_list(title: str, fnames: list) -> bool:
    assert isinstance(title, str)
    assert isinstance(fnames, list)

    tmp = []
    idx = 0
    for name in [basename_of(n) for n in fnames]:
        tmp.append(f"{idx}:{name}")
        idx += 1

    print(title)
    print(" ".join(tmp))

    return True
