"""Format module for contents."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.types.content import ContentRecord, ContentsData
from stobu.types.element import ElmType
from stobu.utils.log import logger


__all__ = (
        'format_contents_data',
        )


# Define Contents
PROC = 'FORMAT CONTENTS'


# Main
def format_contents_data(contents_data: ContentsData) -> list:
    assert isinstance(contents_data, ContentsData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    contents = contents_data.get_data()

    tmp = []

    tmp.append(f"{contents[0].title}\n")
    tmp.append("===\n\n")
    tmp.append("## CONTENTS\n\n")

    for record in contents:
        assert isinstance(record, ContentRecord)
        if ElmType.BOOK is record.type:
            tmp.append(f"### {record.title}\n\n")
        else:
            space = _get_format_space(record.type)
            tmp.append(f"{space}{record.index}. {record.title}\n")

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


# Private Functions
def _get_format_space(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    if ElmType.CHAPTER is elm:
        return ""
    elif ElmType.EPISODE is elm:
        return "    "
    elif ElmType.SCENE is elm:
        return "    " * 2
    else:
        return ""
