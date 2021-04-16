"""Parser of commandline arguments."""

# Official Libraries
from argparse import ArgumentParser, Namespace


# My Modules
from stobu.syss import messages as msg
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'get_commandline_arguments',
        )


# Define Constants
PROC = 'get_commandline_args'
"""str: main process name."""

PROGRAM_NAME = 'stobu'
"""str: program name for argument parser."""

DESCRIPTION = 'story building utility tool on cui.'
"""str: description for argument parser."""


# Main
def get_commandline_arguments() -> Namespace:
    logger.debug(msg.PROC_START.format(proc=PROC))

    parser = assertion.is_instance(_init_commandline_parser(),
            ArgumentParser)

    if not parser:
        return None

    if not _set_parser_options(parser):
        logger.warning(msg.ERR_FAIL_SET_DATA.format(data='arg parser options'))
        return None

    args = parser.parse_args()

    if not args:
        return None

    logger.debug(msg.PROC_DONE.format(proc=PROC))
    return args



# Private Functions
def _init_commandline_parser() -> ArgumentParser:
    _PROC = "init commandline parser"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    parser = ArgumentParser(
            prog=PROGRAM_NAME,
            description=DESCRIPTION,
            )

    logger.debug(msg.PROC_DONE.format(proc=_PROC))
    return parser


def _set_parser_options(parser: ArgumentParser) -> bool:
    assert isinstance(parser, ArgumentParser)
    _PROC = 'set parser options'
    logger.debug(msg.PROC_START.format(proc=_PROC))

    parser.add_argument('cmd', metavar='command', type=str, help='builder command')
    parser.add_argument('elm', metavar='element', type=str, nargs='?', help='sub command or any element')
    parser.add_argument('option', metavar='option', type=str, nargs='?', help='any arguments')
    parser.add_argument('-o', '--outline', help='outline output', action='store_true')
    parser.add_argument('-p', '--plot', help='plot output', action='store_true')
    parser.add_argument('-i', '--info', help='scene info output', action='store_true')
    parser.add_argument('-s', '--script', help='script output', action='store_true')
    parser.add_argument('-n', '--novel', help='novel output', action='store_true')
    parser.add_argument('-r', '--rubi', help='output with rubi', action='store_true')
    parser.add_argument('-v', '--version', help='output app version', action='store_true')
    parser.add_argument('-e', '--edit', help='add and edit when new file', action='store_true')
    parser.add_argument('--part', type=str, help='select ouput part')
    parser.add_argument('--comment', help='show comment', action='store_true')
    parser.add_argument('--debug', help='set debug flag', action='store_true')

    logger.debug(msg.PROC_DONE.format(proc=_PROC))
    return True
