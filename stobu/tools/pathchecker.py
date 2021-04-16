"""Check paths module."""

# Official Libraries
import os


# My Modules
from stobu.tools.pathgetter import filepath_of, filepaths_by_elm
from stobu.types.element import ElmType


__all__ = (
        'is_duplicated_path_in_dir',
        )


# Main
def is_duplicated_path_in_dir(elm: ElmType, fname: str) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    paths = filepaths_by_elm(elm)
    check_path = filepath_of(elm, fname)

    for path in paths:
        if check_path == path:
            return True
    return False
