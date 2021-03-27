"""Main application for storybuilder."""


# Official Libraries
import argparse
import os


# My Modules
from stobu.commands.projectadder import switch_command_to_add
from stobu.commands.projectadder import switch_command_to_copy
from stobu.commands.projectadder import switch_command_to_delete
from stobu.commands.projectadder import switch_command_to_rename
from stobu.commands.projectbuilder import switch_command_to_build
from stobu.commands.projecteditor import switch_command_to_edit, switch_command_to_set_editor
from stobu.commands.projectinitializer import init_project
from stobu.commands.projectpusher import switch_command_to_push
from stobu.commands.projectpusher import switch_command_to_reject
from stobu.commands.projectviewer import switch_command_to_list
from stobu.systems import messages as msg
from stobu.tools import commandlineparser as parse
from stobu.tools.filechecker import exists_project_file
from stobu.util.log import logger


# Define type hints
EXIT_CODE = int


# Define Constants
APP = "Main Application"


# Main
class Application(object):

    """Application for storybuilder."""

    def __init__(self) -> None:
        # base setting
        logger.debug(msg.MSG_INITIALIZED.format(app=APP))

    # main method
    def run(self) -> EXIT_CODE:
        logger.debug(msg.MSG_START_APP.format(app=APP))

        is_succeeded = True
        """bool: if True is successfull result to proceed, False is any
            failure in process.
        """

        # pre process
        cmdargs = parse.get_project_commands()

        if not cmdargs:
            logger.error(msg.ERR_MISSING_DATA.format(data='command'), cmdargs)
            return os.EX_NOINPUT
        assert isinstance(argparse.Namespace)

        logger.debug(
                msg.MSG_SUCCESS_PROC_WITH_DATA.format(proc='get commandline arguments'),
                cmdargs)

        # check if command is init
        if parse.is_init_command(cmdargs.cmd):
            is_succeeded = init_project()
            if not is_succeeded:
                logger.error(msg.ERR_FAILURE_APP_INITIALIZED.format(app='Project'))
                return os.EX_SOFTWARE
            else:
                return os.EX_OK

        # check if project exists
        if not exists_project_file():
            logger.error(msg.ERR_MISSING_DATA.format(data='project file'))
            return os.EX_OSFILE

        # main process
        # - command switch
        is_succeeded = False
        cmd_cache = 'any'

        if parse.is_build_command(cmdargs.cmd):
            is_succeeded = switch_command_to_build(cmdargs)
            cmd_cache = 'build'
        elif parse.is_add_command(cmdargs.cmd):
            is_succeeded = switch_command_to_add(cmdargs)
            cmd_cache = 'add'
        elif parse.is_copy_command(cmdargs.cmd):
            is_succeeded = switch_command_to_copy(cmdargs)
            cmd_cache = 'copy'
        elif parse.is_delete_command(cmdargs.cmd):
            is_succeeded = switch_command_to_delete(cmdargs)
            cmd_cache = 'delete'
        elif parse.is_edit_command(cmdargs.cmd):
            is_succeeded = switch_command_to_edit(cmdargs)
            cmd_cache = 'edit'
        elif parse.is_list_command(cmdargs.cmd):
            is_succeeded = switch_command_to_list(cmdargs)
            cmd_cache = 'list'
        elif parse.is_rename_command(cmdargs.cmd):
            is_succeeded = switch_command_to_rename(cmdargs)
            cmd_cache = 'rename'
        elif parse.is_push_command(cmdargs.cmd):
            is_succeeded = switch_command_to_push(cmdargs)
            cmd_cache = 'push'
        elif parse.is_reject_command(cmdargs.cmd):
            is_succeeded = switch_command_to_reject(cmdargs)
            cmd_cache = 'reject'
        elif parse.is_set_editor_command(cmdargs.cmd):
            is_succeeded = switch_command_to_set_editor(cmdargs)
            cmd_cache = 'set_editor'
        else:
            logger.error(
                    msg.ERR_UNKNOWN_PROC_WITH_DATA.format(proc='app command'),
                    cmdargs.cmd)
            return os.EX_SOFTWARE

        # post process
        if not is_succeeded:
            logger.error(msg.ERR_FAILURE_PROC.format(proc=f'{cmd_cache} command'))
            return os.EX_SOFTWARE

        return os.EX_OK
