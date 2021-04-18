"""Reject file module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.elmchecker import is_enable_elm_in, elm_from
from stobu.tools.orderdatareader import get_filenames_in_order_by_elm
from stobu.tools.orderdatareader import orderitem_of, rid_prefix
from stobu.tools.orderdatawriter import remove_item_order_data, write_order_data
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import get_target_filename_from_list
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.filepath import basename_of
from stobu.utils.log import logger


__all__ = (
        'reject_story_source',
        )


# Define Constants
PROC = 'COMMAND REJECT'


ENABLE_ELMS = [
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def reject_story_source(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.REJECT)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)
    fname = _get_reject_filename(elm, args.option)
    if not fname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"reject filename in {PROC}"))
        return False

    if not _reject_file(elm, fname):
        logger.error(msg.ERR_FAIL_CANNOT_REMOVE_DATA.format(data=f"reject file in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _get_reject_filename(elm: ElmType, fname: str) -> str:
    assert isinstance(elm, ElmType)

    ordernames = [rid_prefix(orderitem_of(elm), name) for name in get_filenames_in_order_by_elm(elm)]

    _fname = assertion.is_str(fname) if fname else get_target_filename_from_list(f"reject {str(elm)}",
            ordernames)

    if not is_duplicated_path_in_dir(elm, _fname):
        logger.warning(msg.ERR_FAIL_CANNOT_WRITE_DATA_WITH_DATA.format(data=f"reject filename in {PROC}"),
                _fname)
        return ""
    return _fname


def _reject_file(elm: ElmType, fname: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    updated = remove_item_order_data(orderitem_of(elm), fname)
    if not write_order_data(updated):
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"write order data in {PROC}"))
        return False
    return True
