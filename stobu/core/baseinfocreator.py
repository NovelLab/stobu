"""Build Base info module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.core.noveler import novels_data_from, outputs_data_from_novels_data
from stobu.core.outliner import outlines_data_from, outputs_data_from_outlines_data
from stobu.core.plotter import plots_data_from, outputs_data_from_plots_data
from stobu.core.scripter import scripts_data_from, outputs_data_from_scripts_data
from stobu.core.structer import structs_data_from, outputs_data_from_structs_data
from stobu.counts.common import counts_data_from
from stobu.elms.books import BookItem
from stobu.formats.novel import format_novels_charcounts_data
from stobu.formats.outline import format_outlines_charcounts_data
from stobu.formats.plot import format_plots_charcounts_data
from stobu.formats.script import format_scripts_charcounts_data
from stobu.formats.struct import format_structs_charcounts_data
from stobu.syss import messages as msg
from stobu.tools.buildchecker import has_build_of
from stobu.tools.datareader import get_basefile_data
from stobu.types.action import ActionsData
from stobu.types.baseinfo import BaseInfoData, BaseInfoRecord, BaseInfoType
from stobu.types.build import BuildType
from stobu.types.element import ElmType
from stobu.types.outline import OutlinesData, OutlineRecord
from stobu.types.output import OutputsData
from stobu.types.story import StoryData, StoryRecord
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'base_info_outputs_data_from',
        )


# Define Constants
PROC = 'BUILD BASE INFO'


# Main
def base_info_outputs_data_from(args: Namespace, story_data: StoryData,
        actions_data: ActionsData, tags: dict) -> OutputsData:
    assert isinstance(args, Namespace)
    assert isinstance(story_data, StoryData)
    assert isinstance(actions_data, ActionsData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = _get_base_info_title()

    columns, rows = _get_columns_rows()

    if has_build_of(args, BuildType.OUTLINE):
        char_counts = _conv_outline_char_counts(story_data, tags, columns, rows)
        if not char_counts or not char_counts.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outlines char count in {PROC}"))
            return None

        tmp += char_counts

    if has_build_of(args, BuildType.PLOT):
        char_counts = _conv_plot_char_counts(story_data, tags, columns, rows)
        if not char_counts or not char_counts.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"plots char count in {PROC}"))
            return None

        tmp += char_counts

    if has_build_of(args, BuildType.STRUCT):
        char_counts = _conv_struct_char_counts(actions_data, tags, columns, rows)
        if not char_counts or not char_counts.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"structs char count in {PROC}"))
            return None

        tmp += char_counts

    if has_build_of(args, BuildType.SCRIPT):
        char_counts = _conv_script_char_counts(actions_data, tags, columns, rows)
        if not char_counts or not char_counts.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"scripts char count in {PROC}"))
            return None

        tmp += char_counts

    if has_build_of(args, BuildType.NOVEL):
        char_counts = _conv_novel_char_counts(actions_data, tags, columns, rows)
        if not char_counts or not char_counts.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"novels char count in {PROC}"))
            return None

        tmp += char_counts

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


# Private Functions
def _conv_novel_char_counts(actions_data: ActionsData, tags: dict,
        columns: int, rows: int) -> OutputsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    novels = novels_data_from(actions_data, tags)
    formatted = outputs_data_from_novels_data(novels, tags)
    novel_counts = counts_data_from(BuildType.NOVEL, formatted, columns, rows)
    if not novel_counts or not novel_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"novels count in {PROC}"))
        return None

    char_counts = OutputsData(format_novels_charcounts_data(novel_counts))
    if not char_counts or not char_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"novels char count in {PROC}"))
        return None

    return char_counts


def _conv_outline_char_counts(story_data: StoryData, tags: dict,
        columns: int, rows: int) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    outlines = outlines_data_from(story_data, tags)
    formatted = outputs_data_from_outlines_data(outlines, tags)
    outline_counts = counts_data_from(BuildType.OUTLINE, formatted, columns, rows)
    if not outline_counts or not outline_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outlines count in {PROC}"))
        return None

    char_counts = OutputsData(format_outlines_charcounts_data(outline_counts))
    if not char_counts or not char_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outlines char count in {PROC}"))
        return None

    return char_counts


def _conv_plot_char_counts(story_data: StoryData, tags: dict,
        columns: int, rows: int) -> OutputsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    plots = plots_data_from(story_data)
    formatted = outputs_data_from_plots_data(plots, tags)
    plot_counts = counts_data_from(BuildType.PLOT, formatted, columns, rows)
    if not plot_counts or not plot_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"plots count in {PROC}"))
        return None

    char_counts = OutputsData(format_plots_charcounts_data(plot_counts))
    if not char_counts or not char_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"plots char count in {PROC}"))
        return None

    return char_counts


def _conv_script_char_counts(actions_data: ActionsData, tags: dict,
        columns: int, rows: int) -> OutputsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    scripts = scripts_data_from(actions_data, tags)
    formatted = outputs_data_from_scripts_data(scripts, tags)
    script_counts = counts_data_from(BuildType.SCRIPT, formatted, columns, rows)
    if not script_counts or not script_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"scripts count in {PROC}"))
        return None

    char_counts = OutputsData(format_scripts_charcounts_data(script_counts))
    if not char_counts or not char_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"scripts char count in {PROC}"))
        return None

    return char_counts


def _conv_struct_char_counts(actions_data: ActionsData, tags: dict,
        columns: int, rows: int) -> OutputsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    structs = structs_data_from(actions_data, tags)
    formatted = outputs_data_from_structs_data(structs, tags)
    struct_counts = counts_data_from(BuildType.STRUCT, formatted, columns, rows)
    if not struct_counts or not struct_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"structs count in {PROC}"))
        return None

    char_counts = OutputsData(format_structs_charcounts_data(struct_counts))
    if not char_counts or not char_counts.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"structs char count in {PROC}"))
        return None

    return char_counts


def _get_base_info_title() -> OutputsData:

    tmp = []

    tmp.append("Base info\n===\n\n")

    return OutputsData(tmp)


def _get_columns_rows() -> tuple:
    data = assertion.is_dict(get_basefile_data(ElmType.BOOK))

    return data[str(BookItem.COLUMNS)], data[str(BookItem.ROWS)]
