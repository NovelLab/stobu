"""Rename file module."""

# Official Libraries
from argparse import Namespace
import os


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.elmchecker import is_enable_elm_in, elm_from
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import filepath_of, filepaths_by_elm, get_target_filename_from_list
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.filepath import new_filename_by_input
from stobu.utils.log import logger


__all__ = (
        'rename_story_source',
        )


# Define Constants
PROC = 'COMMAND RENAME'

ENABLE_ELMS = [
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.EVENT,
        ElmType.ITEM,
        ElmType.NOTE,
        ElmType.OUTLINE,
        ElmType.PERSON,
        ElmType.PLAN,
        ElmType.SCENE,
        ElmType.STAGE,
        ElmType.WORD,
        ]


# Main
def rename_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.RENAME)
    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_rename_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"delete filename in {PROC}"))
        return False

    newname = _get_renamed_name(elm)
    if not newname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"rename name in {PROC}"))
        return False

    if not _rename_file(elm, fname, newname):
        logger.error(msg.ERR_FAIL_CANNOT_REMOVE_DATA.format(data=f"rename file in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _rename_file(elm: ElmType, fname: str, newname: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)
    assert isinstance(newname, str)

    path = filepath_of(elm, fname)
    newpath = filepath_of(elm, newname)

    if newpath != path:
        os.rename(path, newpath)
        return True
    else:
        logger.error(
                msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"rename file in {PROC}"),
                newpath)
        return False


def _get_rename_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    filenames = filepaths_by_elm(elm)

    _fname = assertion.is_str(fname) if fname else get_target_filename_from_list(f"rename {str(elm)}", filenames)

    if not is_duplicated_path_in_dir(elm, _fname):
        logger.warning(
                msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"rename filename in {PROC}"),
                _fname)
        return ""
    return _fname


def _get_renamed_name(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    _fname = new_filename_by_input(str(elm))

    if is_duplicated_path_in_dir(elm, _fname):
        logger.warning(
                msg.ERR_FAIL_DUPLICATED_DATA.format(data=f"new name for renaming in {PROC}"))
        return ""
    return _fname
