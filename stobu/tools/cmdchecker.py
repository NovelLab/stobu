"""Check module for command."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.types.command import CmdType


__all__ = (
        'has_cmd_of',
        )

# Define Constants
COMMAND_TABLE = {
        CmdType.ADD: ('a', 'add'),
        CmdType.BUILD: ('b', 'build'),
        CmdType.COPY: ('c', 'copy'),
        CmdType.DELETE: ('d', 'delete'),
        CmdType.EDIT: ('e', 'edit'),
        CmdType.INIT: ('i', 'init'),
        CmdType.LIST: ('l', 'list'),
        CmdType.PUSH: ('p', 'push'),
        CmdType.REJECT: ('r', 'reject'),
        CmdType.RENAME: ('n', 'rename'),
        CmdType.SET: ('set',),
        CmdType.NONE: ('none',),
        }



# Main
def has_cmd_of(args: Namespace, cmd: CmdType) -> bool:
    assert isinstance(args, Namespace)
    assert isinstance(cmd, CmdType)

    order_cmd = args.cmd

    return order_cmd in COMMAND_TABLE[cmd]
