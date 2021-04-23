"""Common module for info."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoType, InfoRecord
from stobu.utils.log import logger


__all__ = (
        'get_record_as_data_title',
        'get_record_as_splitter',
        )


# Define Constants
PROC = 'INFO COMMON'


# Main
def get_record_as_data_title(title: str) -> InfoRecord:
    assert isinstance(title, str)

    return InfoRecord(InfoType.DATA_TITLE, ActType.DATA,
            f"## {title}", '', '')


def get_record_as_splitter() -> InfoRecord:
    return InfoRecord(InfoType.SPLITTER, ActType.DATA, '', '', '')
