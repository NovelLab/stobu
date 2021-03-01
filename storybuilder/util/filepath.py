"""Utility module for file paths."""


# Official Libraries
import os

# My Modules


__all__ = (
        'add_extention',
        'conv_filenames_from_fullpaths',
        'conv_only_basename',
        'get_current_path',
        'has_extention',
        'is_exists_path',
        )


def add_extention(filename: str, ext: str) -> str:
    '''Add the extention to the filename.
    '''
    return f"{filename}.{ext}"


def basename_of(filepath: str) -> str:
    """Get file name only, except extention and directory name."""
    return os.path.splitext(os.path.basename(filepath))[0]


def conv_filenames_from_fullpaths(paths: list) -> list:
    '''Get file name list that converted from fullpath list.
    '''
    tmp = []
    for name in paths:
        tmp.append(conv_only_basename(name))
    sorted_tmp = sorted(tmp)
    return sorted_tmp


def get_current_path() -> str:
    """Get current path."""
    return os.getcwd()


def get_input_filename(msg: str) -> str:
    """Get user input a string."""
    return input(msg)


def has_extention(filename: str, ext: str) -> bool:
    '''Check the filename has the extention.
    '''
    return f".{ext}" in filename


def is_exists_path(filepath: str) -> bool:
    """Check the file exists."""
    return os.path.exists(filepath)
