"""Commandline arguments and option parser."""


# Official Libraries
import argparse
from typing import Union


# My Modules
from stobu.systems import messages as msg
from stobu.util.log import logger


# Define Constants
PROGRAM_NAME = 'stobu'
"""str: program name for argument parser."""

DESCRIPTION = """
story building manager on cui.
"""
"""str: description for argument parser."""

# Define constants
APP = 'Argument Parser'


# Main Function
def get_project_commands() -> Union[argparse.Namespace, None]:
    logger.debug(msg.MSG_START_APP.format(app=APP))
    parser = _get_commandline_parser()

    if not _init_commandline_parser(parser):
        logger.error(msg.ERR_FAILURE_APP_INITIALIZED(app=APP))
        return None

    return _get_commandline_arguments(parser)


# Check Functions
def is_add_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('a', 'add')


def is_build_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('b', 'build')


def is_copy_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('c', 'copy')


def is_delete_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('d', 'delete')


def is_edit_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('e', 'edit')


def is_init_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('i', 'init')


def is_list_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('l', 'list')


def is_rename_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('n', 'rename')


def is_push_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('p', 'push')


def is_reject_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('r', 'reject')


def is_set_editor_command(cmd: str) -> bool:
    assert isinstance(cmd, str)

    return cmd in ('set_editor',)


# Private Functions
def _get_commandline_parser() -> argparse.ArgumentParser:
    """Argument Parser getter."""

    parser = argparse.ArgumentParser(
            prog=PROGRAM_NAME,
            description=DESCRIPTION,
            )

    logger.debug(msg.MSG_SUCCESS_PROC_WITH_DATA.format(proc=APP), parser)
    return parser


def _init_commandline_parser(parser: argparse.ArgumentParser) -> bool:
    """Init argument parser."""
    assert isinstance(parser, argparse.ArgumentParser)

    parser.add_argument('cmd', metavar='command', type=str, help='builder command')
    parser.add_argument('arg0', metavar='arg0', type=str, nargs='?', help='sub command or any arguments')
    parser.add_argument('arg1', metavar='arg1', type=str, nargs='?', help='any arguments')
    parser.add_argument('-o', '--outline', help='outline output', action='store_true')
    parser.add_argument('-p', '--plot', help='plot output', action='store_true')
    parser.add_argument('-i', '--info', help='scene info output', action='store_true')
    parser.add_argument('-s', '--script', help='script output', action='store_true')
    parser.add_argument('-n', '--novel', help='novel output', action='store_true')
    parser.add_argument('-r', '--rubi', help='output with rubi', action='store_true')
    parser.add_argument('-v', '--version', help='output app version', action='store_true')
    parser.add_argument('--part', type=str, help='select ouput part')
    parser.add_argument('--debug', help='set debug flag', action='store_true')

    logger.debug(msg.MSG_SUCCESS_PROC.format(proc=f'{APP} setting options'))
    return True


def _get_commandline_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Get commandline arguments and parsed list."""
    assert isinstance(parser, argparse.ArgumentParser)

    args = parser.parse_args()

    return args
