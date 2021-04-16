"""Deta read module."""

# Official Libraries
import yaml
from typing import Any


# My Modules
from stobu.elms.orders import OrderItem
from stobu.elms.persons import PersonItem
from stobu.elms.projects import ProjectItem
from stobu.syss import messages as msg
from stobu.syss.settings import PROJECT
from stobu.tools.filedatareader import read_markdown_data_as_yaml, read_yaml_data
from stobu.tools.pathgetter import filepath_of
from stobu.types.element import ElmType
from stobu.utils.fileio import read_file
from stobu.utils.log import logger


__all__ = (
        'get_mob_data',
        'get_order_data',
        'get_person_data',
        'get_project_data',
        'get_time_data',
        'person_item_of',
        'project_item_of',
        )


# Define Constants
PROC = 'TOOL DATA READER'


# Main Functions
def get_mob_data() -> dict:
    return read_yaml_data(read_file(filepath_of(ElmType.MOB, '')))


def get_order_data() -> dict:
    data = read_file(filepath_of(ElmType.ORDER, ''))
    return read_yaml_data(data)[str(OrderItem.BOOK)]


def get_person_data(fname: str) -> dict:
    assert isinstance(fname, str)

    return read_markdown_data_as_yaml(read_file(filepath_of(ElmType.PERSON, fname)))


def get_project_data() -> dict:
    data = read_file(filepath_of(ElmType.PROJECT, ''))
    return yaml.safe_load(data)[PROJECT]


def get_time_data() -> dict:
    return read_yaml_data(read_file(filepath_of(ElmType.TIME, '')))


def person_item_of(fname: str, item: PersonItem) -> Any:
    assert isinstance(fname, str)
    assert isinstance(item, PersonItem)

    data = yaml.safe_load(read_file(filepath_of(ElmType.PERSON, fname)))
    if str(item) in data:
        return data[str(item)]
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"{item} in {PROC}"))
        return ""


def project_item_of(item: ProjectItem) -> Any:
    assert isinstance(item, ProjectItem)

    return get_project_data()[str(item)]
