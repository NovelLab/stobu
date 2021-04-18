"""Data write module."""

# Official Libraries
import yaml


# My Modules
from stobu.elms.projects import ProjectItem
from stobu.syss import messages as msg
from stobu.syss.settings import PROJECT
from stobu.tools.pathgetter import filepath_of
from stobu.types.element import ElmType
from stobu.utils.fileio import read_file, write_file
from stobu.utils.log import logger


__all__ = (
        'write_project_data',
        )


# Define Constants
PROC = 'TOOL WRITE DATA'


# Main
def write_project_data(item: ProjectItem, val: str) -> bool:
    assert isinstance(item, ProjectItem)
    assert isinstance(val, str)

    data = _get_project_raw_data()

    if str(item) in data[PROJECT]:
        data[PROJECT][str(item)] = val

    if not write_file(filepath_of(ElmType.PROJECT, ''), yaml.safe_dump(data)):
        logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"project data in {PROC}"))
        return False
    return True


# Private Functions
def _get_project_raw_data() -> dict:
    data = read_file(filepath_of(ElmType.PROJECT, ''))
    return yaml.safe_load(data)
