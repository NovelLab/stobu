"""Check module for commandline arguments."""

# Official Libraries
import argparse


# My Modules
from stobu.systems import messages as msg
from stobu.util.log import logger


___all__ = (
        'is_command_of',
        'is_init_command',
        )


# Main Functions
def is_command_of(cmd: str, arg: argparse.Namespace) -> bool:
    assert isinstance(cmd, str)
    assert isinstance(arg, argparse.Namespace)

    if 'build' == cmd:
        return arg.cmd in ('b', 'build')
    elif 'add' == cmd:
        return arg.cmd in ('a', 'add')
    elif 'copy' == cmd:
        return arg.cmd in ('c', 'copy')
    elif 'delete' == cmd:
        return arg.cmd in ('d', 'delete')
    elif 'edit' == cmd:
        return arg.cmd in ('e', 'edit')
    elif 'list' == cmd:
        return arg.cmd in ('l', 'list')
    elif 'rename' == cmd:
        return arg.cmd in ('n', 'rename')
    elif 'push' == cmd:
        return arg.cmd in ('p', 'push')
    elif 'reject' == cmd:
        return arg.cmd in ('r', 'reject')
    elif 'set_editor' == cmd:
        return arg.cmd in ('set_editor',)
    else:
        logger.error(msg.ERR_UNKNOWN_PROC_WITH_DATA.format(proc='command'), arg.cmd)
        return False


def is_init_command(arg: argparse.Namespace) -> bool:
    assert isinstance(arg, argparse.Namespace)

    return arg.cmd in ('i', 'init')
