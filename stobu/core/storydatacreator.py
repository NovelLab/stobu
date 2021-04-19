"""Story data create module."""

# Official Libraries
from argparse import Namespace
from dataclasses import dataclass


# My Modules
from stobu.core.orderdataserializer import serialized_filenames_from_order
from stobu.elms.orders import OrderItem
from stobu.elms.scenes import SceneItem
from stobu.syss import messages as msg
from stobu.tools.filedatareader import read_yaml_data, read_markdown_data_as_yaml
from stobu.tools.orderdatareader import elm_from_ordername, rid_prefix, orderitem_of
from stobu.tools.pathgetter import filepath_of
from stobu.tools.storydatareader import scene_item_of, copy_scene_data_of_story_record
from stobu.types.element import ElmType
from stobu.types.story import StoryData, StoryRecord
from stobu.utils import assertion
from stobu.utils.datetimes import next_day_str_from, next_month_str_from, after_day_str_from
from stobu.utils.fileio import read_file
from stobu.utils.log import logger


__all__ = (
        'story_data_from',
        )


# Define Constants
PROC = 'STORY DATA CREATOR'

MAX_NUM = 10000

TOP_LEVEL_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ]

SAME_TAGS = ['-', '_same_', '同']

NEXT_YEAR = ['_next_', '_nextyear_', '翌年']

NEXT_DAY = ['_next_', '_nextday_', '翌日']

NEXT_WEEK = ['_nextweek_', '翌週']

NEXT_MONTH = ['_nextmonth_', '翌月']


@dataclass
class ElmPart(object):
    chapter: tuple = (0, MAX_NUM)
    episode: tuple = (0, MAX_NUM)
    scene: tuple = (0, MAX_NUM)


# Main
def story_data_from(args: Namespace) -> StoryData:
    assert isinstance(args, Namespace)

    logger.debug(msg.PROC_START.format(proc=PROC))

    order_data = read_yaml_data(read_file(filepath_of(ElmType.ORDER, '')))

    if not order_data:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"order data in {PROC}"))
        return None

    elmpart = assertion.is_instance(_get_elm_part(args.part if args.part else ""),
            ElmPart)

    serialized = assertion.is_list(serialized_filenames_from_order(order_data,
            elmpart.chapter[0], elmpart.chapter[1],
            elmpart.episode[0], elmpart.episode[1],
            elmpart.scene[0], elmpart.scene[1],
            ))

    if not serialized:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"serialized data in {PROC}"))
        return None

    story_data_base = _conv_story_data_from(serialized)
    if not story_data_base:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"story data base in {PROC}"))
        return None

    updated = update_story_data_if_same_or_next_tag(StoryData(story_data_base))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return updated


def update_story_data_if_same_or_next_tag(story_data: StoryData) -> StoryData:
    assert isinstance(story_data, StoryData)

    tmp = []
    cache = None

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if record.type in TOP_LEVEL_ELMS:
            tmp.append(record)
        elif record.type is ElmType.SCENE:
            ret = _copy_and_change_scene_data_if_same_or_next(record, cache)
            tmp.append(ret)
            cache = ret
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
            continue

    return StoryData(tmp)


# Private Functions
def _conv_story_data_from(serialized: list) -> list:
    assert isinstance(serialized, list)

    tmp = []
    tmp.append(_conv_story_record_from(str(OrderItem.BOOK)))

    for ordername in serialized:
        tmp.append(_conv_story_record_from(ordername))

    return tmp


def _conv_story_record_from(ordername: str) -> StoryRecord:
    assert isinstance(ordername, str)

    elm = elm_from_ordername(ordername)
    fname = rid_prefix(orderitem_of(elm), ordername)
    data = _get_data_from(elm, fname)

    return StoryRecord(elm, fname, data)


def _copy_and_change_scene_data_if_same_or_next(record: StoryRecord, cache: StoryRecord) -> StoryRecord:
    assert isinstance(record, StoryRecord)
    if not cache:
        return record

    assert isinstance(cache, StoryRecord)

    camera = scene_item_of(record, SceneItem.CAMERA)
    stage = scene_item_of(record, SceneItem.STAGE)
    year = scene_item_of(record, SceneItem.YEAR)
    date = scene_item_of(record, SceneItem.DATE)
    time = scene_item_of(record, SceneItem.TIME)

    if _is_same_tag(camera):
        camera = scene_item_of(cache, SceneItem.CAMERA)

    if _is_same_tag(stage):
        stage = scene_item_of(cache, SceneItem.STAGE)

    if isinstance(year, str) and _is_same_tag(year):
        year = scene_item_of(cache, SceneItem.YEAR)
    elif year in NEXT_YEAR:
        year = str(int(scene_item_of(cache, SceneItem.YEAR)) + 1)

    year = str(year)
    if _is_same_tag(date):
        date = scene_item_of(cache, SceneItem.DATE)
    elif date in NEXT_DAY:
        mon, day = _get_day_and_month_from(cache)
        date = next_day_str_from(year, mon, day)
    elif date in NEXT_WEEK:
        mon, day = _get_day_and_month_from(cache)
        date = after_day_str_from(year, mon, day, 0, 7)
    elif date in NEXT_MONTH:
        mon, day = _get_day_and_month_from(cache)
        date = after_day_str_from(year, mon, day, 1, 0)
    # TODO: after xx

    if _is_same_tag(time):
        time = scene_item_of(cache, SceneItem.TIME)

    return copy_scene_data_of_story_record(
            record, camera, stage, year, date, time)


def _get_data_from(elm: ElmType, fname: str) -> dict:
    assert isinstance(elm, ElmType)
    assert isinstance(fname, str)

    raw_data = read_file(filepath_of(elm, fname))

    if ElmType.BOOK is elm:
        return read_yaml_data(raw_data)
    else:
        return read_markdown_data_as_yaml(raw_data)


def _get_day_and_month_from(record: StoryRecord) -> tuple:
    assert isinstance(record, StoryRecord)

    return scene_item_of(record, SceneItem.DATE).split('/')


def _get_elm_part(order_part: str) -> ElmPart:
    assert isinstance(order_part, str)

    tmp = order_part.split(':')
    elmpart = ElmPart()
    key = ''

    for v in tmp:
        if v in ('c', 'ch', 'chapter'):
            key = 'c'
        elif v in ('e', 'ep', 'episode'):
            key = 'e'
        elif v in ('s', 'sc', 'scene'):
            key = 's'
        else:
            continue

    if key:
        _, start, end = "", "", ""
        if len(order_part) > 3:
            _, start, end = tmp[0], tmp[1], tmp[2]
        else:
            _, start = tmp[0], tmp[1]
            end = start
        _start = 0 if int(start) < 0 else int(start)
        _end = MAX_NUM if int(end) < 0 else int(end)
        if 'c' == key:
            elmpart.chapter = (_start, _end)
        elif 'e' == key:
            elmpart.episode = (_start, _end)
        elif 's' == key:
            elmpart.scene = (_start, _end)
    return elmpart


def _is_same_tag(text: str) -> bool:
    assert isinstance(text, str)

    return text in SAME_TAGS
