"""Format module for outline data."""

# Official Libraries


# My Modules
from stobu.formats.common import head_string_from_elm, get_format_record_as_br
from stobu.formats.common import conv_charcounts_from
from stobu.formats.common import get_breakline
from stobu.syss import messages as msg
from stobu.types.count import CountRecord, CountsData
from stobu.types.element import ElmType
from stobu.types.outline import OutlineRecord, OutlinesData
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'format_outlines_data',
        'format_outlines_charcounts_data',
        )


# Define Constants
PROC = 'FORMAT OUTLINE'


ENABLE_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def format_outlines_charcounts_data(counts_data: CountsData) -> list:
    assert isinstance(counts_data, CountsData)

    _PROC = f"{PROC}: format data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    current = ElmType.NONE

    tmp.append(get_breakline())
    tmp.append("# OUTLINE char counts:\n")

    for record in counts_data.get_data():
        assert isinstance(record, CountRecord)
        if current is not record.type:
            tmp.append(get_format_record_as_br())
            tmp.append(head_string_from_elm(record.type, 'count'))
            current = record.type
        tmp.append(conv_charcounts_from(record))
        tmp.append(get_format_record_as_br())

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


def format_outlines_data(outlines_data: OutlinesData) -> list:
    assert isinstance(outlines_data, OutlinesData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    current = ElmType.NONE

    for record in outlines_data.get_data():
        assert isinstance(record, OutlineRecord)
        if current is not record.type:
            tmp.append(head_string_from_elm(record.type, 'outlines'))
            current = record.type
        tmp.extend(_conv_output_record(record))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


# Private Functions
def _conv_output_record(record: OutlineRecord) -> list:
    assert isinstance(record, OutlineRecord)

    tmp = []

    tmp.append(_record_title_of(record))
    tmp.append(_record_outline_of(record))
    tmp.append(get_format_record_as_br())

    return tmp


def _record_outline_of(record: OutlineRecord) -> str:
    assert isinstance(record, OutlineRecord)

    outline = assertion.is_str(record.outline)

    if not outline:
        return ""

    indent = "    "
    if "\n" in outline:
        lines = outline.split('\n')
        return indent + f"\n{indent}".join(lines) + "\n"
    else:
        return indent + outline + "\n"


def _record_title_of(record: OutlineRecord) -> str:
    assert isinstance(record, OutlineRecord)

    return f"**{record.title}**\n"
