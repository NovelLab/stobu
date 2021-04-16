"""Build outline module."""

# Official Libraries


# My Modules
from stobu.formats.outline import format_outlines_data
from stobu.syss import messages as msg
from stobu.tools.elmchecker import is_enable_the_elm
from stobu.tools.storydatareader import elm_outline_of, elm_title_of
from stobu.tools.translater import translate_tags_str, translate_tags_text_list
from stobu.types.element import ElmType
from stobu.types.outline import OutlineRecord, OutlinesData
from stobu.types.output import OutputsData
from stobu.types.story import StoryData, StoryRecord
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'outlines_data_from',
        'outputs_data_from_outlines_data',
        )


# Define Constants
PROC = 'BUILD OUTLINE'


ENABLE_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def outlines_data_from(story_data: StoryData, tags: dict) -> OutlinesData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        ret = _conv_outline_record(record)
        if ret:
            tmp.append(ret)

    if not tmp:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outline data in {PROC}"))
        return None

    reordered = _reorder_outlines_data(OutlinesData(tmp))
    if not reordered or not reordered.has_data():
        logger.error(msg.ERR_FAILED_PROC.format(proc=f"reorder data in {PROC}"))
        return None

    translated = _translate_outlines_data(reordered, tags)
    if not translated or not translated.has_data():
        logger.error(msg.ERR_FAILED_PROC.format(proc=f"translate data in {PROC}"))
        return None

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return translated


def outputs_data_from_outlines_data(outlines_data: OutlinesData, tags: dict) -> OutputsData:
    assert isinstance(outlines_data, OutlinesData)
    assert isinstance(tags, dict)

    _PROC = f"{PROC}: convert outputs data"
    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    formatted = format_outlines_data(outlines_data)
    if not formatted:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outputs data in {PROC}"))
        return None

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


# Private Functions
def _conv_outline_record(record: StoryRecord) -> OutlineRecord:
    assert isinstance(record, StoryRecord)

    elm = assertion.is_instance(record.type, ElmType)
    if not is_enable_the_elm(elm, ENABLE_ELMS):
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
        return None

    title = assertion.is_str(elm_title_of(record))
    outline = assertion.is_str(elm_outline_of(record))

    return OutlineRecord(elm, title, outline)


def _reorder_outlines_data(outlines_data: OutlinesData) -> OutlinesData:
    assert isinstance(outlines_data, OutlinesData)

    tmp = []

    for elm in ENABLE_ELMS:
        for record in outlines_data.get_data():
            assert isinstance(record, OutlineRecord)
            if elm is record.type:
                tmp.append(record)

    return OutlinesData(tmp)


def _translate_outlines_data(outlines_data: OutlinesData, tags: dict) -> OutlinesData:
    assert isinstance(outlines_data, OutlinesData)
    assert isinstance(tags, dict)

    tmp = []

    for record in outlines_data.get_data():
        assert isinstance(record, OutlineRecord)
        tmp.append(_translate_record(record, tags))

    return OutlinesData(tmp)


def _translate_record(record: OutlineRecord, tags: dict) -> OutlineRecord:
    assert isinstance(record, OutlineRecord)
    assert isinstance(tags, dict)

    return OutlineRecord(
            record.type,
            translate_tags_str(record.title, tags),
            translate_tags_str(record.outline, tags),
            )
