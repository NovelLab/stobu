"""Copy file module."""

# Official Libraries
from argparse import Namespace
import shutil


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.elmchecker import has_elm_of, is_enable_elm_in, elm_from
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import filepath_of, filepaths_by_elm, get_target_filename_from_list
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'copy_story_source',
        )


# Define Constants
PROC = 'COMMAND COPY'


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
def copy_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.COPY)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_copy_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"copy filename in {PROC}"))
        return False

    newname = _get_copied_name(elm, fname)
    if not newname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"copy name in {PROC}"))
        return False

    if not _copy_file(elm, fname, newname):
        logger.error(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"copy {elm} file in {PROC}"))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _copy_file(elm: ElmType, fname: str, newname: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)
    assert isinstance(newname, str)

    shutil.copy(filepath_of(elm, fname), filepath_of(elm, newname))
    return True


def _get_copy_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    filenames = filepaths_by_elm(elm)

    _fname = assertion.is_str(fname) if fname else get_target_filename_from_list(f"copy {str(elm)}", filenames)

    if not is_duplicated_path_in_dir(elm, _fname):
        logger.warning(
                msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"copy filename in {PROC}"),
                _fname)
        return ""
    return _fname


def _get_copied_name(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    for idx in range(100):
        newname = f"{fname}_{idx}"
        if not is_duplicated_path_in_dir(elm, newname):
            return newname
    return ""
