"""Application class."""

# Official Libraries
import os
from argparse import Namespace


# My Modules
from stobu.commands.adder import add_story_source
from stobu.commands.builder import build_project
from stobu.commands.copier import copy_story_source
from stobu.commands.deleter import delete_story_source
from stobu.commands.editor import edit_story_source
from stobu.commands.initializer import init_project
from stobu.commands.lister import show_list_of_story_sources
from stobu.commands.pusher import push_story_source
from stobu.commands.rejector import reject_story_source
from stobu.commands.renamer import rename_story_source
from stobu.commands.setter import set_project_data
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.commandlineparser import get_commandline_arguments
from stobu.types.command import CmdType
from stobu.utils.log import logger


__all__ = (
        'Application',
        )


# Define Constants
PROC = 'APPLICATION'


# Main
class Application(object):

    def __init__(self):
        logger.debug(msg.PROC_INITIALIZED.format(proc=PROC))

    def run(self) -> int:
        logger.debug(msg.PROC_START.format(proc=PROC))

        args = get_commandline_arguments()

        if not args:
            logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"commandline args in {PROC}"))
            return os.EX_NOINPUT

        if has_cmd_of(args, CmdType.INIT):
            if not init_project(args):
                logger.error(msg.ERR_FAIL_CANNOT_INITIALIZE.format(data='project'))
                return os.EX_SOFTWARE
            return os.EX_OK

        is_succeeded = False

        if has_cmd_of(args, CmdType.BUILD):
            is_succeeded = build_project(args)
        elif has_cmd_of(args, CmdType.NONE) or has_cmd_of(args, CmdType.INIT):
            is_succeeded = True
        else:
            if not _is_valid_args(args):
                return os.EX_NOINPUT

            if has_cmd_of(args, CmdType.ADD):
                is_succeeded = add_story_source(args)
            elif has_cmd_of(args, CmdType.COPY):
                is_succeeded = copy_story_source(args)
            elif has_cmd_of(args, CmdType.DELETE):
                is_succeeded = delete_story_source(args)
            elif has_cmd_of(args, CmdType.EDIT):
                is_succeeded = edit_story_source(args)
            elif has_cmd_of(args, CmdType.LIST):
                is_succeeded = show_list_of_story_sources(args)
            elif has_cmd_of(args, CmdType.PUSH):
                is_succeeded = push_story_source(args)
            elif has_cmd_of(args, CmdType.REJECT):
                is_succeeded = reject_story_source(args)
            elif has_cmd_of(args, CmdType.RENAME):
                is_succeeded = rename_story_source(args)
            elif has_cmd_of(args, CmdType.SET):
                is_succeeded = set_project_data(args)
            else:
                logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"command type in {PROC}"))

        if not is_succeeded:
            logger.error(msg.ERR_FAILED_PROC.format(proc=PROC))
            return os.EX_SOFTWARE

        logger.debug(msg.PROC_DONE.format(proc=PROC))
        return os.EX_OK


# Private Functions
def _is_valid_args(args: Namespace) -> bool:
    assert isinstance(args, Namespace)

    if not args.cmd:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"command in {PROC}"))
        return False

    if not args.elm:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"command args in {PROC}"))
        return False

    return True
