"""Push module for storybuilder project."""


# Official Libraries
import argparse
import copy


# My Modules
from stobu.dataconverter import conv_to_dumpdata_of_yaml
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import read_file_as_auto, write_file
from stobu.util.filepath import basename_of, get_input_filename
from stobu.util.log import logger


__all__ = (
        'switch_command_to_push',
        'switch_command_to_reject',
        )


# Define Constants
INPUT_TARGET_FILENAME_WITH_LIST_MESSAGE = \
        "{target_list}\nEnter {target} file name: "
"""str: message to get the deleting file name."""

START_PUSH_PROCESS_MESSAGE = "Pushing the {target} file..."
"""str: message to start pushing process."""

FINISH_PUSH_PROCESS_MESSAGE = "...Succeeded push {target} file."
"""str: message to finish the pushing process as successfull."""

START_REJECT_PROCESS_MESSAGE = "Rejecting the {target} file..."
"""str: message to start rejecting process."""

FINISH_REJECT_PROCESS_MESSAGE = "...Succeeded reject {target} file."
"""str: message to finish the rejecting process as successfull."""

ERR_MESSAGE_DUPLICATED = "Already the {target} file exists!: %s"
"""str: error message when the file already exists."""

ERR_MESSAGE_MISSING_FILE = "Not Found the {target} file!: %s"
"""str: error message when the file not found."""

ERR_MESSAGE_CANNOT_PUSH = "Failed to push the {target} file!: %s"
"""str: error message when the file cannot push."""

ERR_MESSAGE_CANNOT_REJECT = "Failed to reject the {target} file!: %s"
"""str: error message when the file cannot reject."""

ERR_MESSAGE_CANNOT_OVERWRITE = "Failed to overwrite the order file!"
"""str: error message when the order file cannot overwrite."""


# Main Function
def switch_command_to_push(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('p', 'push')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = push_the_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = push_the_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = push_the_scene(cmdargs.arg1)
    else:
        logger.error("Unknown push command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command push!")
        return False

    logger.debug("...Succeeded command push.")
    return True


def switch_command_to_reject(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('j', 'reject')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = reject_the_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = reject_the_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = reject_the_scene(cmdargs.arg1)
    else:
        logger.error("Unknown reject command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command reject!")
        return False

    logger.debug("...Succeeded command reject.")
    return True


# Functions
# - Push
def push_the_chapter(fname: str) -> bool:
    logger.debug(START_PUSH_PROCESS_MESSAGE.format(target="chapter"))

    order_data = read_file_as_auto(ppath.get_order_path())
    tmp = copy.deepcopy(order_data)
    if not _has_the_key('book', tmp) or not _validate_order_book(tmp):
        logger.debug("Invalid order data!: %s", tmp)
        return False

    chapters = ppath.get_chapter_file_names()
    _fname = fname if fname else _get_target_filename(fname, "pushing chapter", chapters)

    if not checker.is_exists_the_chapter(_fname):
        logger.debug(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    if _is_exists_the_chapter_in_order(tmp, _fname):
        logger.debug(ERR_MESSAGE_DUPLICATED.format(target="chapter"), _fname)
        return False

    if not _push_chapter_to_book(tmp, _fname):
        logger.debug(ERR_MESSAGE_CANNOT_PUSH.format(target="chapter"), _fname)
        return False

    if not write_file(ppath.get_order_path(), conv_to_dumpdata_of_yaml(tmp)):
        logger.debug(ERR_MESSAGE_CANNOT_OVERWRITE)
        return False

    logger.debug(FINISH_PUSH_PROCESS_MESSAGE.format(target="chapter"))
    return True


def push_the_episode(fname: str) -> bool:
    logger.debug(START_PUSH_PROCESS_MESSAGE.format(target="episode"))

    order_data = read_file_as_auto(ppath.get_order_path())
    tmp = copy.deepcopy(order_data)
    if not _has_the_key('book', tmp) or not _validate_order_book(tmp):
        logger.debug("Invalid order data!: %s", tmp)
        return False

    episodes = ppath.get_episode_file_names()
    _fname = fname if fname else _get_target_filename(fname, "pushing episode", episodes)

    if not checker.is_exists_the_episode(_fname):
        logger.debug(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    if _is_exists_the_episode_in_order(tmp, _fname):
        logger.debug(ERR_MESSAGE_DUPLICATED.format(target="episode"), _fname)
        return False

    chapters = _get_chapter_names_from_order(tmp)
    _ch_name = _get_target_filename("", "pushed chapter", chapters)

    if not _push_episode_to_chapter(tmp, _fname, _ch_name):
        logger.debug(ERR_MESSAGE_CANNOT_PUSH.format(target="episode"), _fname)
        return False

    if not write_file(ppath.get_order_path(), conv_to_dumpdata_of_yaml(tmp)):
        logger.debug(ERR_MESSAGE_CANNOT_OVERWRITE)
        return False

    logger.debug(FINISH_PUSH_PROCESS_MESSAGE.format(target="episode"))
    return True


def push_the_scene(fname: str) -> bool:
    logger.debug(START_PUSH_PROCESS_MESSAGE.format(target="scene"))

    order_data = read_file_as_auto(ppath.get_order_path())
    tmp = copy.deepcopy(order_data)
    if not _has_the_key('book', tmp) or not _validate_order_book(tmp):
        logger.debug("Invalid order data!: %s", tmp)
        return False

    scenes = ppath.get_scene_file_names()
    _fname = fname if fname else _get_target_filename(fname, "pushing scene", scenes)

    if not checker.is_exists_the_scene(_fname):
        logger.debug(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    if _is_exists_the_scene_in_order(tmp, _fname):
        logger.debug(ERR_MESSAGE_DUPLICATED.format(target="scene"), _fname)
        return False

    episodes = _get_episode_names_from_order(tmp)
    _ep_name = _get_target_filename("", "pushed episode", episodes)

    if not _push_scene_to_episode(tmp, _fname, _ep_name):
        logger.debug(ERR_MESSAGE_CANNOT_PUSH.format(target="scene"), _fname)
        return False

    if not write_file(ppath.get_order_path(), conv_to_dumpdata_of_yaml(tmp)):
        logger.debug(ERR_MESSAGE_CANNOT_OVERWRITE)
        return False

    logger.debug(FINISH_PUSH_PROCESS_MESSAGE.format(target="scene"))
    return True


# - Reject
def reject_the_chapter(fname: str) -> bool:
    logger.debug(START_REJECT_PROCESS_MESSAGE.format(target="chapter"))

    order_data = read_file_as_auto(ppath.get_order_path())
    tmp = copy.deepcopy(order_data)
    if not _has_the_key('book', tmp) or not _validate_order_book(tmp):
        logger.error("Invalid order data!: %s", tmp)
        return False

    chapters = _get_chapter_names_from_order(tmp)
    _fname = fname if fname else _get_target_filename(fname, "rejecting chapter", chapters)

    if not _is_exists_the_chapter_in_order(tmp, _fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="chapter"), _fname)
        return False

    if not _reject_chapter_from_order(tmp, _fname):
        logger.error(ERR_MESSAGE_CANNOT_REJECT.format(target="chapter"), _fname)
        return False

    if not write_file(ppath.get_order_path(), conv_to_dumpdata_of_yaml(tmp)):
        logger.error(ERR_MESSAGE_CANNOT_OVERWRITE)
        return False

    logger.debug(FINISH_REJECT_PROCESS_MESSAGE.format(target="chapter"))
    return True


def reject_the_episode(fname: str) -> bool:
    logger.debug(START_REJECT_PROCESS_MESSAGE.format(target="episode"))

    order_data = read_file_as_auto(ppath.get_order_path())
    tmp = copy.deepcopy(order_data)
    if not _has_the_key('book', tmp) or not _validate_order_book(tmp):
        logger.error("Invalid order data!: %s", tmp)
        return False

    episodes = _get_episode_names_from_order(tmp)
    _fname = fname if fname else _get_target_filename(
            fname, "rejectiong episode", episodes)

    if not _is_exists_the_episode_in_order(tmp, _fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="episode"), _fname)
        return False

    if not _reject_episode_from_order(tmp, _fname):
        logger.error(ERR_MESSAGE_CANNOT_REJECT.format(target="episode"), _fname)
        return False

    if not write_file(ppath.get_order_path(), conv_to_dumpdata_of_yaml(tmp)):
        logger.error(ERR_MESSAGE_CANNOT_OVERWRITE)
        return False

    logger.debug(FINISH_REJECT_PROCESS_MESSAGE.format(target="episode"))
    return True


def reject_the_scene(fname: str) -> bool:
    logger.debug(START_REJECT_PROCESS_MESSAGE.format(target="scene"))

    order_data = read_file_as_auto(ppath.get_order_path())
    tmp = copy.deepcopy(order_data)
    if not _has_the_key('book', tmp) or not _validate_order_book(tmp):
        logger.error("Invalid order data!: %s", tmp)
        return False

    scenes = _get_scene_names_from_order(tmp)
    _fname = fname if fname else _get_target_filename(
            fname, "rejecting scene", scenes)

    if not _is_exists_the_scene_in_order(tmp, _fname):
        logger.error(ERR_MESSAGE_MISSING_FILE.format(target="scene"), _fname)
        return False

    if not _reject_scene_from_order(tmp, _fname):
        logger.error(ERR_MESSAGE_CANNOT_REJECT.format(target="scene"), _fname)
        return False

    if not write_file(ppath.get_order_path(), conv_to_dumpdata_of_yaml(tmp)):
        logger.error(ERR_MESSAGE_CANNOT_OVERWRITE)
        return False

    logger.debug(FINISH_REJECT_PROCESS_MESSAGE.format(target="scene"))
    return True


# Private Function
def _chaptername_of(fname: str) -> str:
    assert isinstance(fname, str)

    return f"chapter/{basename_of(fname)}"


def _episodename_of(fname: str) -> str:
    assert isinstance(fname, str)

    return f"episode/{basename_of(fname)}"


def _get_chapter_names_from_order(orderdata: dict) -> list:
    assert isinstance(orderdata, dict)

    tmp = []

    for ch_record in assertion.is_list(orderdata['book']):
        assert isinstance(ch_record, dict)
        for key in ch_record.keys():
            prefix, name = assertion.is_str(key).split('/')
            tmp.append(name)
    return tmp


def _get_episode_names_from_order(orderdata: dict) -> list:
    assert isinstance(orderdata, dict)

    tmp = []

    for ch_record in assertion.is_list(orderdata['book']):
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                for key in ep_record.keys():
                    prefix, name = assertion.is_str(key).split('/')
                    tmp.append(name)
    return tmp


def _get_scene_names_from_order(orderdata: dict) -> list:
    assert isinstance(orderdata, dict)

    tmp = []

    for ch_record in assertion.is_list(orderdata['book']):
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                for ep_data in ep_record.values():
                    assert isinstance(ep_data, list)
                    for sc_record in ep_data:
                        prefix, name = assertion.is_str(sc_record).split('/')
                        tmp.append(name)
    return tmp


def _get_target_filename(fname: str, msg: str, targets: list) -> str:
    tmp = []
    idx = 0
    for t in targets:
        tmp.append(f"{idx}:{t}")
        idx += 1
    _fname = assertion.is_str(fname) if fname else get_input_filename(
            INPUT_TARGET_FILENAME_WITH_LIST_MESSAGE.format(
                target=msg, target_list=" ".join(tmp)))
    if _fname.isnumeric():
        if 0 <= int(_fname) < len(targets):
            return targets[int(_fname)]
        else:
            return _fname
    else:
        return _fname


def _has_the_key(key: str, data: dict) -> bool:
    assert isinstance(key, str)
    assert isinstance(data, dict)

    return key in data


def _is_exists_the_chapter_in_order(orderdata: dict, fname: str) -> bool:
    """Check if the chapter in order."""
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    _fname = _chaptername_of(fname)

    for ch_record in orderdata['book']:
        assert isinstance(ch_record, dict)

        if _fname in ch_record.keys():
            return True
    return False


def _is_exists_the_episode_in_order(orderdata: dict, fname: str) -> bool:
    """Check if the episode in order."""
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    _fname = _episodename_of(fname)

    for ch_record in orderdata['book']:
        assert isinstance(ch_record, dict)

        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)

            for ep_record in ch_data:
                assert isinstance(ep_record, dict)

                if _fname in ep_record.keys():
                    return True
    return False


def _is_exists_the_scene_in_order(orderdata: dict, fname: str) -> bool:
    """Check if the scene in order."""
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    _fname = _scenename_of(fname)

    for ch_record in orderdata['book']:
        assert isinstance(ch_record, dict)

        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)

            for ep_record in ch_data:
                assert isinstance(ep_record, dict)

                for ep_data in ep_record.values():
                    assert isinstance(ep_data, list)

                    for scene_name in ep_data:
                        if _fname == scene_name:
                            return True
    return False


def _push_chapter_to_book(orderdata: dict, fname: str) -> bool:
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    assertion.is_list(orderdata['book']).append({_chaptername_of(fname): []})

    return True


def _push_episode_to_chapter(
        orderdata: dict, fname: str, ch_name: str) -> bool:
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)
    assert isinstance(ch_name, str)

    _ch_name = _chaptername_of(ch_name)

    for ch_record in orderdata['book']:
        assert isinstance(ch_record, dict)
        if _ch_name in ch_record.keys():
            assertion.is_list(ch_record[_ch_name]).append(
                    {_episodename_of(fname): []})
            return True
    return False


def _push_scene_to_episode(orderdata: dict, fname: str, ep_name: str) -> bool:
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)
    assert isinstance(ep_name, str)

    _ep_name = _episodename_of(ep_name)

    for ch_record in orderdata['book']:
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                if _ep_name in ep_record.keys():
                    assertion.is_list(ep_record[_ep_name]).append(
                            _scenename_of(fname))
                    return True
    return False


def _reject_chapter_from_order(orderdata: dict, fname: str) -> bool:
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    _ch_name = _chaptername_of(fname)
    tmp = []

    for ch_record in assertion.is_list(orderdata['book']):
        assert isinstance(ch_record, dict)
        if _ch_name not in ch_record.keys():
            tmp.append(ch_record)
    orderdata['book'] = tmp
    return True


def _reject_episode_from_order(orderdata: dict, fname: str) -> bool:
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    _ep_name = _episodename_of(fname)

    for ch_record in assertion.is_list(orderdata['book']):
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            tmp = []
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                if _ep_name not in ep_record.keys():
                    tmp.append(ep_record)
            for key in ch_record.keys():
                ch_record[key] = tmp
    return True


def _reject_scene_from_order(orderdata: dict, fname: str) -> bool:
    assert isinstance(orderdata, dict)
    assert isinstance(fname, str)

    _sc_name = _scenename_of(fname)

    for ch_record in assertion.is_list(orderdata['book']):
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                for ep_data in ep_record.values():
                    assert isinstance(ep_data, list)
                    tmp = []
                    for sc_record in ep_data:
                        assert isinstance(sc_record, str)
                        if sc_record != _sc_name:
                            tmp.append(sc_record)
                    for key in ep_record.keys():
                        ep_record[key] = tmp
    return True


def _scenename_of(fname: str) -> str:
    assert isinstance(fname, str)

    return f"scene/{basename_of(fname)}"


def _validate_order_book(orderdata: dict) -> bool:
    assert isinstance(orderdata, dict)

    if not orderdata['book']:
        orderdata['book'] = []

    return True
