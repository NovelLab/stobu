"""Format module for plot data."""

# Official Libraries


# My Modules
from stobu.formats.common import head_string_from_elm
from stobu.formats.common import get_breakline
from stobu.formats.common import get_format_record_as_br, head_string_from_elm
from stobu.formats.common import conv_charcounts_from
from stobu.syss import messages as msg
from stobu.types.count import CountRecord, CountsData
from stobu.types.element import ElmType
from stobu.types.plot import PlotsData, PlotRecord
from stobu.utils.log import logger
from stobu.utils.strings import get_indent_text


__all__ = (
        'format_plots_data',
        'format_plots_charcounts_data',
        )


# Define Constants
PROC = 'FORMAT PLOT'


ENABLE_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def format_plots_charcounts_data(counts_data: CountsData) -> list:
    assert isinstance(counts_data, CountsData)

    _PROC = f"{PROC}: format data"
    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    current = ElmType.NONE

    tmp.append(get_breakline())
    tmp.append("# PLOT char counts:\n")

    for record in counts_data.get_data():
        assert isinstance(record, CountRecord)
        if not current is record.type:
            tmp.append(get_format_record_as_br())
            tmp.append(head_string_from_elm(record.type, 'count'))
            current = record.type
        tmp.append(conv_charcounts_from(record))
        tmp.append(get_format_record_as_br())

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


def format_plots_data(plots_data: PlotsData) -> list:
    assert isinstance(plots_data, PlotsData)

    tmp = []
    current = ElmType.NONE

    for record in plots_data.get_data():
        assert isinstance(record, PlotRecord)
        if not current is record.type:
            tmp.append(head_string_from_elm(record.type, record.title))
            current = record.type
        tmp.extend(_conv_output_record(record))

    return tmp


# Private Functions
def _conv_output_record(record: PlotRecord) -> list:
    assert isinstance(record, PlotRecord)

    tmp = []

    tmp.append(_record_title_of(record))
    tmp.extend(_record_plot_of(record))
    tmp.append('\n')

    return tmp


def _record_plot_of(record: PlotRecord) -> list:

    tmp = []
    space = "    "

    tmp.append(f"{get_indent_text(record.setup)}\n")
    tmp.append(f"{space}↓＜{record.tp1st}＞\n")
    tmp.append(f"{get_indent_text(record.develop)}\n")
    tmp.append(f"{space}↓＜{record.tp2nd}＞\n")
    tmp.append(f"{get_indent_text(record.climax)}\n")
    tmp.append(f"{space}→＜{record.resolve}＞\n")

    return tmp


def _record_title_of(record: PlotRecord) -> str:
    assert isinstance(record, PlotRecord)

    return f"**{record.title}**\n"
