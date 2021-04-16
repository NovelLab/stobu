"""Read story data and record module."""

# Official Libraries
from typing import Any
import copy


# My Modules
from stobu.elms.books import BookItem
from stobu.elms.chapters import ChapterItem
from stobu.elms.episodes import EpisodeItem
from stobu.elms.events import EventItem
from stobu.elms.items import ItemItem
from stobu.elms.notes import NoteItem
from stobu.elms.outlines import OutlineItem
from stobu.elms.persons import PersonItem
from stobu.elms.plans import PlanItem
from stobu.elms.scenes import SceneItem
from stobu.elms.stages import StageItem
from stobu.elms.words import WordItem
from stobu.syss import messages as msg
from stobu.types.element import ElmType
from stobu.types.story import StoryRecord
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'copy_scene_data_of_story_record',
        'elm_data_of',
        'elm_outline_of',
        'elm_plot_of',
        'elm_title_of',
        'scene_item_of',
        )


# Define Constants
PROC = 'TOOL STORY DATA READER'

DATAS = {
        ElmType.BOOK: "",
        ElmType.CHAPTER: ChapterItem.DATA,
        ElmType.EPISODE: EpisodeItem.DATA,
        ElmType.EVENT: EventItem.DATA,
        ElmType.ITEM: ItemItem.DATA,
        ElmType.NOTE: NoteItem.DATA,
        ElmType.OUTLINE: OutlineItem.DATA,
        ElmType.PERSON: PersonItem.DATA,
        ElmType.PLAN: PlanItem.DATA,
        ElmType.SCENE: SceneItem.DATA,
        ElmType.STAGE: StageItem.DATA,
        ElmType.WORD: WordItem.DATA,
        }


OUTLINES = {
        ElmType.BOOK: BookItem.OUTLINE,
        ElmType.CHAPTER: ChapterItem.OUTLINE,
        ElmType.EPISODE: EpisodeItem.OUTLINE,
        ElmType.SCENE: SceneItem.OUTLINE,
        }


PLOTS = {
        ElmType.BOOK: BookItem.PLOT,
        ElmType.CHAPTER: ChapterItem.PLOT,
        ElmType.EPISODE: EpisodeItem.PLOT,
        ElmType.SCENE: SceneItem.PLOT,
        }


TITLES = {
        ElmType.BOOK: BookItem.TITLE,
        ElmType.CHAPTER: ChapterItem.TITLE,
        ElmType.EPISODE: EpisodeItem.TITLE,
        ElmType.EVENT: EventItem.NAME,
        ElmType.ITEM: ItemItem.NAME,
        ElmType.NOTE: NoteItem.NAME,
        ElmType.OUTLINE: OutlineItem.NAME,
        ElmType.PERSON: PersonItem.NAME,
        ElmType.PLAN: PlanItem.NAME,
        ElmType.SCENE: SceneItem.TITLE,
        ElmType.STAGE: StageItem.NAME,
        ElmType.WORD: WordItem.NAME,
        }


# Main
def copy_scene_data_of_story_record(record: StoryRecord,
        camera: str = None,
        stage: str = None,
        year: (int, str) = None,
        date: str = None,
        time: str = None) -> StoryRecord:
    assert isinstance(record, StoryRecord)

    tmp = copy.deepcopy(record.data)

    if camera:
        tmp[str(SceneItem.CAMERA)] = camera
    if stage:
        tmp[str(SceneItem.STAGE)] = stage
    if year:
        tmp[str(SceneItem.YEAR)] = year
    if date:
        tmp[str(SceneItem.DATE)] = date
    if time:
        tmp[str(SceneItem.TIME)] = time

    return StoryRecord(record.type, record.filename, tmp)


def elm_data_of(record: StoryRecord) -> list:
    return assertion.is_list(_safe_get_elm_item_of(record, DATAS))


def elm_outline_of(record: StoryRecord) -> str:
    return assertion.is_str(_safe_get_elm_item_of(record, OUTLINES))


def elm_plot_of(record: StoryRecord) -> dict:
    return assertion.is_dict(_safe_get_elm_item_of(record, PLOTS))


def elm_title_of(record: StoryRecord) -> str:
    return assertion.is_str(_safe_get_elm_item_of(record, TITLES))


def scene_item_of(record: StoryRecord, item: SceneItem) -> str:
    assert isinstance(record, StoryRecord)
    assert isinstance(item, SceneItem)

    if str(item) in record.data:
        return record.data[str(item)]
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"scene item in {PROC}"))
        return ""


# Private Functions
def _safe_get_elm_item_of(record: StoryRecord, item_table: dict) -> Any:
    assert isinstance(record, StoryRecord)
    assert isinstance(item_table, dict)

    key = str(item_table[record.type])
    if key in record.data:
        return record.data[key]
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"{key} data in {PROC}"))
        return ""
