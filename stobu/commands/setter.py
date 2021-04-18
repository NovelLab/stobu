"""Set project data module."""

# Official Libraries
from argparse import Namespace
from enum import auto, Enum

# My Modules
from stobu.elms.projects import ProjectItem
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.datareader import project_item_of
from stobu.tools.datawriter import write_project_data
from stobu.types.command import CmdType
from stobu.utils.log import logger


__all__ = (
        'set_project_data',
        )


# Define Constants
PROC = 'COMMAND SET'


class SetElmType(Enum):
    NONE = auto()
    EDITOR = auto()


SET_ELMS = {
        SetElmType.EDITOR: ('e', 'editor'),
        }


# Main
def set_project_data(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.SET)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not _is_enable_setelm(args):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"set element type in {PROC}"))
        return False

    elm = _setelm_from(args)
    is_succeeded = False

    if SetElmType.EDITOR is elm:
        is_succeeded = set_editor()
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"set element type in {PROC}"))

    if not is_succeeded:
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


# Sub processes
def set_editor() -> bool:
    name = project_item_of(ProjectItem.EDITOR)

    newname = _get_new_editorname(name)
    if not newname:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"in {PROC}"))
        return False

    if not write_project_data(ProjectItem.EDITOR, newname):
        logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"new editor name in {PROC}"))
        return False

    return True


# Private Functions
def _get_new_editorname(name: str) -> str:
    assert isinstance(name, str)

    _name = input(f"> Please Enter changing new editor name from '{name}': ")
    if not _name:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"new editor name in {PROC}"))
        return ""
    return _name


def _is_enable_setelm(args: Namespace) -> bool:
    assert isinstance(args, Namespace)

    elm = args.elm
    for setelm in SET_ELMS.values():
        if elm in setelm:
            return True
    return False


def _setelm_from(args: Namespace) -> SetElmType:
    assert isinstance(args, Namespace)

    elm = args.elm
    for key, setelm in SET_ELMS.items():
        if elm in setelm:
            return key
    return SetElmType.NONE
