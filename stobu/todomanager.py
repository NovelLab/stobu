"""Manager module for storybuilder todo."""


# Official Libraries
import re


# My Modules
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import read_file_as_auto, write_file
from stobu.util.log import logger


__all__ = (
        'add_todo',
        'show_list_of_todo',
        )


# Define Constants
HEAD_TITLE = "ToDo list\n====\n"
"""str: head string of file title."""

HEAD_USER_TODO = "## User Todo"
"""str: head string of user todo."""

HEAD_CONTENTS_STEPS = "## Contents step"
"""str: head string of contents step."""

HEAD_DATA_STEP = "## Data step"
"""str: head string of data step."""


# Main Functions
def add_todo(todo: str) -> bool:
    logger.debug("Starting to add Todo...")

    _todo = assertion.is_str(todo) if todo else input("Enter new todo: ")

    if not _todo:
        return False

    data = _get_todo_data()
    data['users'].append(_todo)

    updated = _construct_todo_data(data)

    if not write_file(ppath.get_todo_path(), "".join(updated)):
        logger.error("...Failed to write the todo file!")
        return False

    logger.debug("...Succeeded to add Todo.")
    return True


def show_list_of_todo() -> bool:
    logger.debug("Starting to show todo list...")

    data = assertion.is_dict(_get_todo_data())
    tmp = assertion.is_list(data['users'])
    print(f"{HEAD_TITLE}")
    for line in tmp:
        print(line)

    logger.debug("...Succeeded to show todo list.")
    return True


# Private Functions
def _construct_todo_data(data: dict) -> str:
    tmp = []

    tmp.append(HEAD_TITLE)

    tmp.append(f"{HEAD_USER_TODO}\n\n")
    for line in data['users']:
        _line = line
        if '[ ]' in _line:
            tmp.append(f"{_line}\n")
        elif '[x]' in _line:
            tmp.append(f"{_line}\n")
        else:
            tmp.append(f"- [ ] {_line}\n")

    tmp.append('\n')
    tmp.append(f"{HEAD_CONTENTS_STEPS}\n\n")
    for line in data['contents']:
        tmp.append(f"{line}\n")

    tmp.append('\n')
    tmp.append(f"{HEAD_DATA_STEP}\n\n")
    for line in data['datas']:
        _line = line
        if '[ ]' in _line:
            tmp.append(f"{_line}\n")
        elif '[x]' in _line:
            tmp.append(f"{_line}\n")
        else:
            tmp.append(f"- [ ] {_line}\n")

    return tmp


def _get_todo_data() -> dict:
    data = assertion.is_dict(read_file_as_auto(ppath.get_todo_path()))
    todos = {
            'users': [],
            'contents': [],
            'datas': [],
            }
    in_current = ''

    for line in assertion.is_list(data['markdown']):
        assert isinstance(line, str)
        if line in ('', '\n', '\r', '\n\r'):
            continue
        if HEAD_USER_TODO in line:
            in_current = 'users'
        elif HEAD_CONTENTS_STEPS in line:
            in_current = 'contents'
        elif HEAD_DATA_STEP in line:
            in_current = 'datas'
        elif 'users' == in_current:
            todos['users'].append(line)
        elif 'contents' == in_current:
            todos['contents'].append(line)
        elif 'datas' == in_current:
            todos['datas'].append(line)
        else:
            continue

    return todos
