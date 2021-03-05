"""Commandline arguments and option parser."""


# Official Libraries
import argparse
from typing import Union


# My Modules
from stobu.util.log import logger


# Define Constants
PROGRAM_NAME = 'stobu'
"""str: program name for argument parser."""

DESCRIPTION = """
story building manager on cui.
"""
"""str: description for argument parser."""


# main function
def get_project_commands() -> Union[argparse.Namespace, None]:
    logger.debug("Starting get commandline arguments...")
    parser = get_commandline_parser()

    if not init_commandline_parser(parser):
        logger.error("Failed the initializing commandline parser!")
        return None

    return get_commandline_arguments(parser)


# functions
def get_commandline_parser() -> argparse.ArgumentParser:
    """Argument Parser getter."""

    parser = argparse.ArgumentParser(
            prog=PROGRAM_NAME,
            description=DESCRIPTION,
            )

    logger.debug("Create an ArgumentParser.")
    return parser


def init_commandline_parser(parser: argparse.ArgumentParser) -> bool:
    """Init argument parser."""
    assert isinstance(parser, argparse.ArgumentParser)

    parser.add_argument('cmd', metavar='command', type=str, help='builder command')
    parser.add_argument('arg0', metavar='arg0', type=str, nargs='?', help='sub command or any arguments')
    parser.add_argument('arg1', metavar='arg1', type=str, nargs='?', help='any arguments')
    parser.add_argument('-o', '--outline', help='outline output', action='store_true')
    parser.add_argument('-p', '--plot', help='plot output', action='store_true')
    parser.add_argument('-s', '--script', help='script output', action='store_true')
    parser.add_argument('-n', '--novel', help='novel output', action='store_true')
    parser.add_argument('-r', '--rubi', help='output with rubi', action='store_true')
    parser.add_argument('-v', '--version', help='output app version', action='store_true')
    parser.add_argument('--part', type=str, help='select ouput part')
    parser.add_argument('--debug', help='set debug flag', action='store_true')

    logger.debug("Initialized the ArgumentParser.")
    return True


def get_commandline_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Get commandline arguments and parsed list."""
    assert isinstance(parser, argparse.ArgumentParser)

    args = parser.parse_args()

    return args
