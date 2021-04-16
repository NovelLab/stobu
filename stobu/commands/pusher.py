"""Push file module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.elmchecker import has_elm_of, is_enable_elm_in, elm_from
from stobu.tools.orderdatareader import get_filenames_in_order_by_elm
from stobu.tools.orderdatareader import get_parent_item_of, ordername_of, orderitem_of
from stobu.tools.orderdatareader import get_elm_from_order, rid_prefix
from stobu.tools.orderdatawriter import add_order_data, write_order_data
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import filepath_of, filepaths_by_elm, get_target_filename_from_list
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.filepath import basename_of
from stobu.utils.log import logger


__all__ = (
        'push_story_source',
        )


# Define Constants
PROC = 'COMMAND PUSH'


ENABLE_ELMS = [
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def push_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.PUSH)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_push_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"push filename in {PROC}"))
        return False

    parent = 'book'

    if not ElmType.CHAPTER is elm:
        parent = _get_push_parent_filename(elm)
        if not parent:
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"push parent filename in {PROC}"))
            return False

    if not _push_file(elm, fname, parent):
        logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"push file in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _get_push_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    filenames = [basename_of(name) for name in filepaths_by_elm(elm)]
    ordernames = [rid_prefix(orderitem_of(elm), name) for name in get_filenames_in_order_by_elm(elm)]

    _fname = assertion.is_str(fname) if fname else get_target_filename_from_list(f"push {str(elm)}",
        list(set(filenames) - set(ordernames)))

    if not is_duplicated_path_in_dir(elm, _fname):
        logger.warning(msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"push filename in {PROC}"),
                _fname)
        return ""
    return _fname


def _get_push_parent_filename(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    parent_elm = get_elm_from_order(get_parent_item_of(orderitem_of(elm)))
    ordernames = [rid_prefix(orderitem_of(parent_elm), name) for name in get_filenames_in_order_by_elm(parent_elm)]

    _fname = get_target_filename_from_list("parent name", ordernames)

    if not is_duplicated_path_in_dir(parent_elm, _fname):
        logger.warning(msg.ERR_FAIL_MISSING_DATA_WITH_DATA.format(data=f"parent filename in {PROC}"),
                _fname)
        return ""

    return _fname


def _push_file(elm: ElmType, fname: str, parent: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)
    assert isinstance(parent, str)

    updated = add_order_data(orderitem_of(elm), fname, parent)
    if not write_order_data(updated):
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"write order data in {PROC}"))
        return False

    return True
