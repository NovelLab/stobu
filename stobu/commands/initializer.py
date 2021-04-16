"""Initialize project module."""

# Official Libraries
from argparse import Namespace
import os


# My Modules
from stobu.paths.projects import MARKDOWN_EXT, YAML_EXT
from stobu.paths.projects import DIRS_TABLE
from stobu.paths.projects import BASE_FILE_TABLE
from stobu.syss import messages as msg
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.pathgetter import filepath_of
from stobu.tools.pathgetter import dirpath_of
from stobu.tools.templater import get_template_data
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.utils.fileio import write_file
from stobu.utils.filepath import is_exists_path
from stobu.utils.log import logger


__all__ = (
        'init_project',
        )


# Define Constants
PROC = 'INITIALIZER'


BASE_FILES = [
        ElmType.BOOK,
        ElmType.MOB,
        ElmType.ORDER,
        ElmType.PROJECT,
        ElmType.RUBI,
        ElmType.TIME,
        ElmType.TODO,
        ]


DEFAULT_FILES = [
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.EVENT,
        ElmType.ITEM,
        ElmType.NOTE,
        ElmType.OUTLINE,
        ElmType.PERSON,
        ElmType.PLAN,
        ElmType.SCENE,
        ElmType.STAGE,
        ElmType.WORD,
        ]


# Main
def init_project(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.INIT)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not check_and_create_directories():
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"check and create dirs in {PROC}"))
        return False

    if not check_and_create_default_files():
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"check and create files in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return True


def check_and_create_directories() -> bool:
    _PROC = f"{PROC}: check and create dirs"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    for elm, dirpath in DIRS_TABLE.items():
        if dirpath:
            if not _safe_create_directory(dirpath_of(elm)):
                logger.error(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"{dirpath} in {_PROC}"))
                return False

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return True


def check_and_create_default_files() -> bool:
    _PROC = f"{PROC}: check and create files"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    for elm in BASE_FILES:
        path = filepath_of(elm, BASE_FILE_TABLE[elm])
        if not is_exists_path(path):
            data = get_template_data(elm)
            if not write_file(path, data):
                logger.warning(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"{str(elm)} in {_PROC}"))
                return False
        else:
            logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {str(elm)} file in {PROC}"))
            continue

    for elm in DEFAULT_FILES:
        path = filepath_of(elm, 'main')
        if not is_exists_path(path):
            data = get_template_data(elm)
            if not write_file(path, data):
                logger.warning(msg.ERR_FAIL_CANNOT_CREATE_DATA.format(data=f"{str(elm)} in {_PROC}"))
                return False
        else:
            logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {str(elm)} file in {PROC}"))
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return True


# Private Functions
def _safe_create_directory(dirpath: str) -> bool:
    assert isinstance(dirpath, str)

    if not is_exists_path(dirpath):
        os.makedirs(dirpath)
    else:
        logger.debug(msg.PROC_MESSAGE.format(proc=f"Already exists {dirpath} in {PROC}"))

    return True
