"""Show list of files module."""

# Officiali Libraries
from argparse import Namespace
import yaml


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.datareader import get_order_data
from stobu.tools.elmchecker import has_elm_of, is_enable_elm_in, elm_from
from stobu.tools.pathgetter import filepaths_by_elm
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils.filepath import basename_of, filenames_with_number
from stobu.utils.log import logger


__all__ = (
        'show_list_of_story_sources',
        )


# Define Constants
PROC = 'COMMAND LIST'


ENABLE_ELMS = [
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.EVENT,
        ElmType.ITEM,
        ElmType.NOTE,
        ElmType.ORDER,
        ElmType.OUTLINE,
        ElmType.PERSON,
        ElmType.PLAN,
        ElmType.SCENE,
        ElmType.STAGE,
        ElmType.WORD,
        ]


# Main
def show_list_of_story_sources(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.LIST)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not is_enable_elm_in(args, ENABLE_ELMS):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return False

    elm = elm_from(args)

    if not _show_list(elm):
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"show list in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Private Functions
def _show_list(elm: ElmType) -> bool:
    assert isinstance(elm, ElmType)

    if ElmType.ORDER is elm:
        return _show_list_of_order()
    else:
        return _show_list_of_files(elm)

def _show_list_of_files(elm: ElmType) -> bool:
    assert isinstance(elm, ElmType)

    paths = [basename_of(name) for name in filepaths_by_elm(elm)]

    print(f"#### {str(elm)}'s list ####")
    for name in filenames_with_number(paths):
        print(name)
    return True


def _show_list_of_order() -> bool:
    data = yaml.safe_dump(get_order_data())

    print("#### Orders ####")
    print(data)

    return True
