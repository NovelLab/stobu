"""Build Base info module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.core.noveler import novels_data_from, outputs_data_from_novels_data
from stobu.core.outliner import outlines_data_from, outputs_data_from_outlines_data
from stobu.core.plotter import plots_data_from, outputs_data_from_plots_data
from stobu.core.scripter import scripts_data_from, outputs_data_from_scripts_data
from stobu.counts.common import counts_data_from
from stobu.counts.novel import counts_data_from_novels_outputs_data
from stobu.counts.outline import counts_data_from_outlines_outputs_data
from stobu.counts.plot import counts_data_from_plots_outputs_data
from stobu.counts.script import counts_data_from_scripts_outputs_data
from stobu.elms.books import BookItem
from stobu.formats.novel import format_novels_charcounts_data
from stobu.formats.outline import format_outlines_charcounts_data
from stobu.formats.plot import format_plots_charcounts_data
from stobu.formats.script import format_scripts_charcounts_data
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

        tmp += char_counts

    if has_build_of(args, BuildType.PLOT):
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

        tmp += char_counts

    if has_build_of(args, BuildType.SCRIPT):
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

        tmp += char_counts

    if has_build_of(args, BuildType.NOVEL):
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

        tmp += char_counts

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


# Private Functions
def _get_base_info_title() -> OutputsData:

    tmp = []

    tmp.append("Base info\n===\n\n")

    return OutputsData(tmp)


def _get_columns_rows() -> tuple:
    data = assertion.is_dict(get_basefile_data(ElmType.BOOK))

    return data[str(BookItem.COLUMNS)], data[str(BookItem.ROWS)]
