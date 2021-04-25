"""Path get module."""

# Official Libraries
import os
import glob


# My Modules
from stobu.paths.projects import APP_DIR
from stobu.paths.projects import PROJECT_DIR
from stobu.paths.projects import BASE_FILE_TABLE, DIRS_TABLE, EXT_TABLE
from stobu.syss import messages as msg
from stobu.types.element import ElmType, BASE_FILES
from stobu.utils.filepath import basename_of, filenames_with_number
from stobu.utils.log import logger


__all__ = (
        'add_extention',
        'dirpath_of',
        'ext_of',
        'get_app_path',
        'get_project_path',
        'get_target_filename_from_list',
        'filepath_of',
        'filepaths_by_elm',
        'is_base_file',
        )


# Define Constants
PROC = 'TOOL PATH GETTER'


# Main
def add_extention(fname: str, ext: str) -> str:
    assert isinstance(fname, str)
    assert isinstance(ext, str)

    return f"{fname}.{ext}"


def dirpath_of(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    return os.path.join(get_project_path(), DIRS_TABLE[elm])


def ext_of(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    return EXT_TABLE[elm]


def get_app_path() -> str:
    return APP_DIR


def get_project_path() -> str:
    return PROJECT_DIR


def get_target_filename_from_list(title: str, targets: list) -> str:
    assert isinstance(title, str)
    assert isinstance(targets, list)

    _targets = sorted([basename_of(name) for name in targets])
    filenames = " ".join(filenames_with_number(_targets))

    fname = input(f"## {filenames} ##\n> Please Enter the filename of {title}: ")

    if fname and fname.isnumeric():
        idx = int(fname) - 1
        return _targets[idx]
    elif fname:
        return fname
    else:
        return ""


def filepath_of(elm: ElmType, fname: str, ext: str = None) -> str:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    _ext = ext_of(elm)
    if ext:
        assert isinstance(ext, str)
        _ext = ext

    _fname = fname
    if is_base_file(elm):
        _fname = BASE_FILE_TABLE[elm]

    return os.path.join(
            dirpath_of(elm),
            add_extention(basename_of(_fname), _ext))


def filepaths_by_elm(elm: ElmType) -> list:
    assert isinstance(elm, ElmType)

    return glob.glob(
            os.path.join(dirpath_of(elm), f"*.{ext_of(elm)}"))


def is_base_file(elm: ElmType) -> bool:
    assert isinstance(elm, ElmType)

    return elm in BASE_FILES
