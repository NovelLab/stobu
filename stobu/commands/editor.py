"""Edit file module."""

# Official Libraries
from argparse import Namespace
import subprocess


# My Modules
from stobu.elms.projects import ProjectItem
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.datareader import project_item_of
from stobu.tools.elmchecker import is_enable_elm_in, elm_from
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import filepath_of, filepaths_by_elm, get_target_filename_from_list
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'edit_story_source',
        )


# Define Constants
PROC = 'COMMAND EDIT'


ENABLE_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.EVENT,
        ElmType.ITEM,
        ElmType.NOTE,
        ElmType.ORDER,
        ElmType.OUTLINE,
        ElmType.PERSON,
        ElmType.PLAN,
        ElmType.RUBI,
        ElmType.SCENE,
        ElmType.STAGE,
        ElmType.TIME,
        ElmType.TODO,
        ElmType.WORD,
        ]


# Main
def edit_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.EDIT)

    logger.debug(msg.PROC_START.format(proc=PROC))
    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_edit_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"copy filename in {PROC}"))
        return False

    if not _edit_file(elm, fname):
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"edit {elm} file in {PROC}"))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _edit_file(elm: ElmType, fname: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    editor = _get_editor()
    path = filepath_of(elm, fname)
    proc = subprocess.run([editor, path])
    if proc.returncode != 0:
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"edit file in {PROC}"))

    return True


def _get_edit_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    filenames = filepaths_by_elm(elm)

    _fname = assertion.is_str(fname) if fname else get_target_filename_from_list(f"edit {str(elm)}", filenames)

    if not is_duplicated_path_in_dir(elm, _fname):
        logger.warning(
                msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"edit filename in {PROC}"),
                _fname)
        return ""
    return _fname


def _get_editor() -> str:
    return assertion.is_str(project_item_of(ProjectItem.EDITOR))
