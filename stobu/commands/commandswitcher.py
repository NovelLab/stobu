"""Main command switching module."""

# Official Libraries
import argparse
import os
from dataclasses import dataclass


# My Modules
from stobu.commands.commandchecker import is_command_of, is_init_command
from stobu.systems import messages as msg
from stobu.util.log import logger


__all__ = (
        'run_command',
        )


# Define types
@dataclass
class RunResult(object):
    name: str
    result: bool


# Main Functions
def run_command(arg: argparse.Namespace) -> RunResult:
    assert isinstance(arg, argparse.Namespace)

    name = "any"
    result = False

    if is_command_of('build', arg):
        result = switch_command_to_build(arg)
        cmd_cache = 'build'
    elif is_command_of('add', arg):
        result = switch_command_to_add(arg)
        cmd_cache = 'add'
    elif is_command_of('copy', arg):
        result = switch_command_to_copy(arg)
        cmd_cache = 'copy'
    elif is_command_of('delete', arg):
        result = switch_command_to_delete(arg)
        cmd_cache = 'delete'
    elif is_command_of('edit', arg):
        result = switch_command_to_edit(arg)
        cmd_cache = 'edit'
    elif is_command_of('list', arg):
        result = switch_command_to_list(arg)
        cmd_cache = 'list'
    elif is_command_of('rename', arg):
        result = switch_command_to_rename(arg)
        cmd_cache = 'rename'
    elif is_command_of('push', arg):
        result = switch_command_to_push(arg)
        cmd_cache = 'push'
    elif is_command_of('reject', arg):
        result = switch_command_to_reject(arg)
        cmd_cache = 'reject'
    elif is_command_of('set_editor', arg):
        result = switch_command_to_set_editor(arg)
        cmd_cache = 'set_editor'
    else:
        logger.error(
                msg.ERR_UNKNOWN_PROC_WITH_DATA.format(proc='app command'),
                arg.cmd)
        return os.EX_SOFTWARE

    return RunResult(name, result)


def run_init_command(arg: argparse.Namespace) -> RunResult:
    assert isinstance(arg, argparse.Namespace)

    result = False

    if is_init_command(arg):
        result = init_project()
        if not result:
            logger.error(msg.ERR_FAILURE_APP_INITIALIZED.format(app='Project'))
    else:
        result = True

    return RunResult('init', result)
