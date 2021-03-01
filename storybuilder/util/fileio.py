"""Utility module for file IO."""


# Official Libraries
import os
import yaml


# My Modules


__all__ = (
        'read_file',
        'write_file',
        )


# Define Constants
DEFAULT_ENCODING = 'utf-8'


def read_file(fname: str, encoding: str=DEFAULT_ENCODING) -> str:
    """Get the file contents."""
    assert isinstance(fname, str)
    assert isinstance(encoding, str)

    contents = ""

    with open(fname, 'r', encoding=encoding) as file:
        contents = file.read()

    return contents


def read_file_as_markdown(fname: str, encoding: str=DEFAULT_ENCODING) -> dict:
    """Get the file contents by markdown format."""
    assert isinstance(fname, str)
    assert isinstance(encoding, str)

    tmp = []

    with open(fname, 'r', encoding=encoding) as file:
        tmp = file.readlines()

    fronts = []
    bodys = []
    is_frontmatter = False

    for line in tmp:
        assert isinstance(line, str)
        _line = line.rstrip('\n\r')
        if _line == '---':
            if is_frontmatter:
                is_frontmatter = False
                continue
            else:
                is_frontmatter = True
        if is_frontmatter:
            fronts.append(_line)
        else:
            bodys.append(_line)

    if fronts:
        _bodys = yaml.safe_load("\n".join(fronts))
        return {**_bodys, **{'markdown': bodys}}
    else:
        return {'markdown': bodys}


def read_file_as_yaml(fname: str, encoding: str=DEFAULT_ENCODING) -> dict:
    """Get the file contents by yaml format."""
    assert isinstance(fname, str)
    assert isinstance(encoding, str)

    contents = {}

    with open(fname, 'r', encoding=encoding) as file:
        contents = yaml.safe_load(file)

    return contents


def write_file(fname: str, contents: str, encoding: str=DEFAULT_ENCODING) -> bool:
    """Write a text in the file."""
    assert isinstance(fname, str)
    assert isinstance(contents, str)
    assert isinstance(encoding, str)

    with open(fname, 'w', encoding=encoding) as file:
        file.write(contents)

    return True

