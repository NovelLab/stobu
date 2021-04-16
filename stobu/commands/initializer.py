"""Initialize project module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.types.command import CmdType
from stobu.utils.log import logger


__all__ = (
        'init_project',
        )


# Main
def init_project(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.INIT)
    return True
