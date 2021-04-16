"""Build plot module."""

# Official Libraries


# My Modules
from stobu.elms.plots import PlotItem
from stobu.formats.plot import format_plots_data
from stobu.syss import messages as msg
from stobu.tools.elmchecker import is_enable_the_elm
from stobu.tools.storydatareader import elm_title_of, elm_plot_of
from stobu.tools.translater import translate_tags_text_list
from stobu.types.element import ElmType
from stobu.types.output import OutputsData
from stobu.types.plot import PlotsData, PlotRecord
from stobu.types.story import StoryData, StoryRecord
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'plots_data_from',
        'outputs_data_from_plots_data',
        )


# Define Constants
PROC = 'BUILD PLOT'


ENABLE_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def plots_data_from(story_data: StoryData) -> PlotsData:
    assert isinstance(story_data, StoryData)

    tmp = []

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        ret = _conv_plot_record(record)
        if ret:
            tmp.append(ret)

    if not tmp:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"plots data in {PROC}"))
        return None

    return PlotsData(tmp)


def outputs_data_from_plots_data(plots_data: PlotsData, tags: dict) -> OutputsData:
    assert isinstance(plots_data, PlotsData)
    assert isinstance(tags, dict)

    _PROC = f"{PROC}: convert outputs data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    formatted = format_plots_data(plots_data)
    if not formatted:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outputs data in {PROC}"))
        return None

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


# Private Functions
def _conv_plot_record(record: StoryRecord) -> PlotRecord:
    assert isinstance(record, StoryRecord)

    elm = assertion.is_instance(record.type, ElmType)
    if not is_enable_the_elm(elm, ENABLE_ELMS):
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return None

    title = assertion.is_str(elm_title_of(record))
    setup = assertion.is_str(_elm_setup_of(record))
    tp1st = assertion.is_str(_elm_tp1st_of(record))
    develop = assertion.is_str(_elm_develop_of(record))
    tp2nd = assertion.is_str(_elm_tp2nd_of(record))
    climax = assertion.is_str(_elm_climax_of(record))
    resolve = assertion.is_str(_elm_resolve_of(record))

    return PlotRecord(elm, title, setup, tp1st, develop, tp2nd, climax, resolve)


def _elm_climax_of(record: StoryRecord) -> str:
    assert isinstance(record, StoryRecord)

    return _get_plot_item_of(record, PlotItem.CLIMAX)


def _elm_develop_of(record: StoryRecord) -> str:
    assert isinstance(record, StoryRecord)

    return _get_plot_item_of(record, PlotItem.DEVELOP)


def _elm_resolve_of(record: StoryRecord) -> str:
    assert isinstance(record, StoryRecord)

    return _get_plot_item_of(record, PlotItem.RESOLVE)


def _elm_setup_of(record: StoryRecord) -> str:
    assert isinstance(record, StoryRecord)

    return _get_plot_item_of(record, PlotItem.SETUP)


def _elm_tp1st_of(record: StoryRecord) -> str:
    assert isinstance(record, StoryRecord)

    return _get_plot_item_of(record, PlotItem.TP1ST)


def _elm_tp2nd_of(record: StoryRecord) -> str:
    assert isinstance(record, StoryRecord)

    return _get_plot_item_of(record, PlotItem.TP2ND)


def _get_plot_item_of(record: StoryRecord, item: PlotItem) -> str:
    assert isinstance(record, StoryRecord)
    assert isinstance(item, PlotItem)

    data = assertion.is_dict(elm_plot_of(record))

    if not data:
        logger.warning(msg.ERR_FAIL_MISSING_DATA.format(data=f"plot data in {PROC}"))
        return ""

    key = str(item)
    if not key in data:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"{key} of record in {PROC}"))
        return ""

    return data[key]
