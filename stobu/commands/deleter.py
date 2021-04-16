"""Delete file module."""

# Official Libraries
from argparse import Namespace
import shutil


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.elmchecker import is_enable_elm_in, elm_from
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import dirpath_of
from stobu.tools.pathgetter import filepath_of, filepaths_by_elm, get_target_filename_from_list
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'delete_story_source',
        )


# Define Constants
PROC = 'COMMAND DELETE'


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
def delete_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.DELETE)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_remove_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"delete filename in {PROC}"))
        return False

    if not _remove_file(elm, fname):
        logger.error(msg.ERR_FAIL_CANNOT_REMOVE_DATA.format(data=f"remove file in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _get_remove_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    filenames = filepaths_by_elm(elm)

    _fname = assertion.is_str(fname) if fname else get_target_filename_from_list(f"remove {str(elm)}", filenames)

    if not is_duplicated_path_in_dir(elm, _fname):
        logger.warning(
                msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"remove filename in {PROC}"),
                _fname)
        return ""
    return _fname


def _remove_file(elm: ElmType, fname: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    shutil.move(filepath_of(elm, fname), dirpath_of(ElmType.TRASH))

    return True
