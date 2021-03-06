"""Main application for storybuilder."""


# Official Libraries
import os


# My Modules
from stobu.commandlineparser import get_project_commands
from stobu.projectadder import switch_command_to_add
from stobu.projectadder import switch_command_to_copy
from stobu.projectadder import switch_command_to_delete
from stobu.projectadder import switch_command_to_rename
from stobu.projectbuilder import switch_command_to_build
from stobu.projecteditor import switch_command_to_edit
from stobu.projectinitializer import init_project
from stobu.projectpusher import switch_command_to_push
from stobu.projectpusher import switch_command_to_reject
from stobu.projectviewer import switch_command_to_list
from stobu.tools.filechecker import exists_project_file
from stobu.util.log import logger


# Define type hints
EXIT_CODE = int


class Application(object):

    """Application for storybuilder."""

    def __init__(self) -> None:
        # base setting
        logger.debug("Initialized the Application.")

    # main method
    def run(self) -> EXIT_CODE:
        logger.debug("Starting the Application...")

        is_succeeded = True
        """bool: if True is successfull result to proceed, False is any
            failure in process.
        """

        # pre process
        cmdargs = get_project_commands()

        if not cmdargs:
            logger.error("Missing command!: %s", cmdargs)
            return os.EX_NOINPUT

        logger.debug("Success get the command-line arguments: %s", cmdargs)

        # check if command is init
        if cmdargs.cmd in ('i', 'init'):
            logger.debug("INIT project starting...")
            is_succeeded = init_project()
            if not is_succeeded:
                logger.error("Uninitialized this project. we have any problems!")
                return os.EX_SOFTWARE
            else:
                return os.EX_OK

        # check if project exists
        if not exists_project_file():
            logger.error("Missing the project file!")
            return os.EX_OSFILE

        # main process
        # - command switch
        is_succeeded = False

        if cmdargs.cmd in ('b', 'build'):
            is_succeeded = switch_command_to_build(cmdargs)
        elif cmdargs.cmd in ('a', 'add'):
            is_succeeded = switch_command_to_add(cmdargs)
        elif cmdargs.cmd in ('c', 'copy'):
            is_succeeded = switch_command_to_copy(cmdargs)
        elif cmdargs.cmd in ('d', 'delete'):
            is_succeeded = switch_command_to_delete(cmdargs)
        elif cmdargs.cmd in ('e', 'edit'):
            is_succeeded = switch_command_to_edit(cmdargs)
        elif cmdargs.cmd in ('l', 'list'):
            is_succeeded = switch_command_to_list(cmdargs)
        elif cmdargs.cmd in ('r', 'rename'):
            is_succeeded = switch_command_to_rename(cmdargs)
        elif cmdargs.cmd in ('p', 'push'):
            is_succeeded = switch_command_to_push(cmdargs)
        elif cmdargs.cmd in ('j', 'reject'):
            is_succeeded = switch_command_to_reject(cmdargs)
        else:
            logger.error("Unknown command!: %s", cmdargs.cmd)
            return os.EX_SOFTWARE

        # post process
        if not is_succeeded:
            logger.error("Failed any command!")
            return os.EX_SOFTWARE

        return os.EX_OK
