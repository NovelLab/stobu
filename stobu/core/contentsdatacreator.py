"""Contents data create module."""

# Official Libraries


# My Modules
from stobu.elms.books import BookItem
from stobu.elms.chapters import ChapterItem
from stobu.elms.episodes import EpisodeItem
from stobu.elms.scenes import SceneItem
from stobu.formats.common import get_breakline_list
from stobu.formats.content import format_contents_data
from stobu.syss import messages as msg
from stobu.tools.elmchecker import is_enable_the_elm
from stobu.tools.translater import translate_tags_str
from stobu.types.content import ContentsData, ContentRecord
from stobu.types.element import ElmType
from stobu.types.output import OutputsData
from stobu.types.story import StoryData, StoryRecord
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'contents_data_from',
        'outputs_data_from_contents_data',
        )


# Define Constants
PROC = 'CONTENTS CREATOR'


ENABLE_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


TITLE_ELMS = {
        ElmType.BOOK: BookItem.TITLE,
        ElmType.CHAPTER: ChapterItem.TITLE,
        ElmType.EPISODE: EpisodeItem.TITLE,
        ElmType.SCENE: SceneItem.TITLE,
        }


# Main
def contents_data_from(story_data: StoryData, tags: dict) -> ContentsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    contents = _contents_data_from(story_data)
    if not contents or not contents.has_data():
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"contents data in {PROC}"))
        return None

    translated = _translate_contents_data(contents, tags)
    if not translated or not translated.has_data():
        logger.error(msg.ERR_FAIL_SUBPROCESS.format(proc=f"translate data in {PROC}"))
        return None

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return translated


def outputs_data_from_contents_data(contents_data: ContentsData) -> OutputsData:
    assert isinstance(contents_data, ContentsData)

    formatted = assertion.is_list(format_contents_data(contents_data))

    return OutputsData(formatted + get_breakline_list())


# Private Functions
def _content_record_of(record: StoryRecord, index: int) -> ContentRecord:
    assert isinstance(record, StoryRecord)
    assert isinstance(index, int)

    elm = assertion.is_instance(record.type, ElmType)

    if not str(TITLE_ELMS[elm]) in record.data:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"content record in {PROC}"))
        return None

    title = record.data[str(TITLE_ELMS[elm])]

    return ContentRecord(elm, title, index)


def _contents_data_from(story_data: StoryData) -> ContentsData:
    assert isinstance(story_data, StoryData)

    tmp = []
    idx = {
            ElmType.BOOK: 1,
            ElmType.CHAPTER: 1,
            ElmType.EPISODE: 1,
            ElmType.SCENE: 1,
            }

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if is_enable_the_elm(record.type, ENABLE_ELMS):
            ret = _content_record_of(record, idx[record.type])
            if ret:
                tmp.append(ret)
                idx[record.type] += 1
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))

    return ContentsData(tmp)


def _translate_contents_data(contents_data: ContentsData, tags: dict) -> ContentsData:
    assert isinstance(contents_data, ContentsData)
    assert isinstance(tags, dict)

    tmp = []

    for record in contents_data.get_data():
        assert isinstance(record, ContentRecord)
        tmp.append(_translate_record(record, tags))

    return ContentsData(tmp)


def _translate_record(record: ContentRecord, tags: dict) -> ContentRecord:
    assert isinstance(record, ContentRecord)
    assert isinstance(tags, dict)

    return ContentRecord(
            record.type,
            translate_tags_str(record.title, tags),
            record.index,
            )
