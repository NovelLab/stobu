"""Main application for storybuilder."""


# Official Libraries
from argparse import Namespace
import os


# My Modules
from stobu.commands.commandswitcher import run_command, run_init_command
from stobu.commands.commandswitcher import RunResult
from stobu.systems import messages as msg
from stobu.tools import commandlineparser as parse
from stobu.tools.filechecker import exists_project_file
from stobu.util import assertion
from stobu.util.log import logger


# Define type hints
EXIT_CODE = int


# Define Constants
APP = "Main Application"


# Main
class Application(object):

    """Application for storybuilder."""

    def __init__(self) -> None:
        self._args = None
        logger.debug(msg.MSG_INITIALIZED.format(app=APP))

    # Methods
    def run(self) -> EXIT_CODE:
        logger.debug(msg.MSG_START_APP.format(app=APP))

        # pre process
        if not self._pre_process():
            return os.EX_SOFTWARE

        # main process
        if not self._main_process(self._args):
            return os.EX_SOFTWARE

        # post process
        if not self._post_process():
            return os.EX_SOFTWARE

        logger.debug(msg.MSG_FINISH_APP.format(app=APP))
        return os.EX_OK

    # Private Methods
    def _pre_process(self) -> bool:
        logger.debug(msg.MSG_START_PROC.format(proc="Pre Process"))
        args = parse.get_project_commands()

        if not args:
            logger.error(msg.ERR_MISSING_DATA.format(data='command'), args)
            return os.EX_NOINPUT
        assert isinstance(args, Namespace)

        logger.debug(
                msg.MSG_SUCCESS_PROC_WITH_DATA.format(
                    proc='get commandline arguments'), args)

        # check if command is init
        init_result = assertion.is_instance(run_init_command(args), RunResult)
        if not init_result.result:
            return False

        # check if project exists
        if not exists_project_file():
            logger.error(msg.ERR_MISSING_DATA.format(data='project file'))
            return False

        self._args = args

        logger.debug(msg.MSG_FINISH_PROC.format(proc="Pre Process"))
        return True

    def _main_process(self, args: Namespace) -> bool:
        assert isinstance(args, Namespace)
        logger.debug(msg.MSG_START_PROC.format(proc="Main Process"))

        run_result = assertion.is_instance(run_command(args), RunResult)

        if not run_result.result:
            logger.error(msg.ERR_FAILURE_PROC.format(proc=f'{run_result.name} command'))
            return False

        logger.debug(msg.MSG_FINISH_PROC.format(proc="Main Process"))
        return True

    def _post_process(self) -> bool:
        logger.debug(msg.MSG_START_PROC.format(proc="Post Process"))
        logger.debug(msg.MSG_FINISH_PROC.format(proc="Post Process"))
        return True
