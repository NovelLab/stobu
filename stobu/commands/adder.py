"""Add file module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.elmchecker import elm_from, is_enable_elm_in
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import filepath_of
from stobu.tools.templater import get_template_data
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.fileio import write_file
from stobu.utils.filepath import new_filename_by_input
from stobu.utils.log import logger


__all__ = (
        'add_story_source',
        )


# Define Constants
PROC = 'COMMAND ADD'


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
def add_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.ADD)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_new_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA)
        return False

    path = filepath_of(elm, fname)
    data = get_template_data(elm)

    if not write_file(path, data):
        logger.error(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"new {elm} file in {PROC}"))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _get_new_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    _fname = assertion.is_str(fname) if fname else new_filename_by_input(str(elm))

    if is_duplicated_path_in_dir(elm, _fname):
        logger.warning(
                msg.ERR_FAIL_DUPLICATED_DATA_WITH_DATA.format(data=f"new filename in {PROC}"),
                _fname)
        return ""
    return _fname
