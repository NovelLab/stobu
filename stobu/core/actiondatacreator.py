"""Action data create module for storybuilder project."""


# Official Libraries


# My Modules
from stobu.dataconverter import conv_action_record_from_scene_action
from stobu.datatypes import ActionData, ActionRecord
from stobu.datatypes import StoryData, StoryRecord
from stobu.util import assertion
from stobu.util.datetimes import get_next_month_day_str
from stobu.util.log import logger


__all__ = (
        'get_action_data',
        )


# Main Function
def get_action_data(story_data: StoryData) -> ActionData:
    assert isinstance(story_data, StoryData)
    logger.debug("Creating Action data from story data...")

    tmp = []
    scene_cache = None

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if record.category == 'book':
            tmp.append(ActionRecord('book-title', "", "", record.data['title']))
        elif record.category == 'chapter':
            tmp.append(ActionRecord('chapter-title', "", "", record.data['title']))
        elif record.category == 'episode':
            tmp.append(ActionRecord('episode-title', "", "", record.data['title']))
        elif record.category == 'scene':
            ret, head = _get_action_data_in_scene(record, scene_cache)
            if ret:
                tmp.extend(ret)
                scene_cache = head
        else:
            logger.debug("Unknown StoryRecord data!: %s", record)
            continue

    logger.debug("...Succeeded create Action data.")
    return ActionData(tmp)


# Private Functions
def _get_action_data_in_scene(
        record: StoryRecord, cache: StoryRecord) -> (list, StoryRecord):
    assert isinstance(record, StoryRecord)
    assert record.category == 'scene'
    if cache:
        assert isinstance(cache, StoryRecord)
        assert cache.category == 'scene'

    tmp = []
    act_cache = None

    head = assertion.is_list(_get_action_data_of_scene_head(record, cache))
    tmp.extend(head)

    for line in record.data['markdown']:
        assert isinstance(line, str)
        ret = conv_action_record_from_scene_action(line, act_cache)
        if ret:
            assert isinstance(ret, ActionRecord)
            tmp.append(ret)
            act_cache = ret

    tmp.append(ActionRecord('scene-end', ""))

    return tmp, StoryRecord(
            'scene',
            '_cache_',
            {'camera': assertion.is_instance(head[1], ActionRecord).subject,
                'stage': assertion.is_instance(head[2], ActionRecord).subject,
                'year': assertion.is_instance(head[3], ActionRecord).subject,
                'date': assertion.is_instance(head[4], ActionRecord).subject,
                'time': assertion.is_instance(head[5], ActionRecord).subject,
                },
            )


def _get_action_data_of_scene_head(record: StoryRecord, cache: StoryRecord) -> list:
    assert isinstance(record, StoryRecord)
    assert record.category == 'scene'
    if cache:
        assert isinstance(cache, StoryRecord)
        assert cache.category == 'scene'

    camera = record.data['camera']
    stage = record.data['stage']
    year = record.data['year']
    date = record.data['date']
    time = record.data['time']

    if cache:
        if camera == '_same_':
            camera = cache.data['camera']
        if stage == '_same_':
            stage = cache.data['stage']
        if year == '_same_':
            year = cache.data['year']
        elif '_next' in str(year) or str(year) in ('翌年', '一年後', '二年後', '三年後', '四年後', '五年後', '十年後'):
            if year in ('_nextyear_', '翌年', '一年後'):
                year = cache.data['year'] + 1
            elif year in ('_next2year_', '二年後'):
                year = cache.data['year'] + 2
            elif year in ('_next3year_', '三年後'):
                year = cache.data['year'] + 3
            elif year in ('_next4year_', '四年後'):
                year = cache.data['year'] + 4
            elif year in ('_next5year_', '五年後'):
                year = cache.data['year'] + 5
            elif year in ('_next10year_', '十年後'):
                year = cache.data['year'] + 10
        if date == '_same_':
            date = cache.data['date']
        elif '_next' in date or date in ('翌日', '翌週', '翌月'):
            m, d = cache.data['date'].split('/')
            if date in ('_nextday_', '翌日'):
                date = get_next_month_day_str(str(year), m, d, 0, 1)
            elif date in ('_nextweek_', '翌週'):
                date = get_next_month_day_str(str(year), m, d, 0, 7)
            elif date in ('_nextmonth_', '翌月'):
                date = get_next_month_day_str(str(year), m, d, 1, 0)
        if time == '_same_':
            time = cache.data['time']

    tmp = []
    tmp.append(ActionRecord('scene-title', "", "", record.data['title']))
    tmp.append(ActionRecord('scene-camera', camera))
    tmp.append(ActionRecord('scene-stage', stage))
    tmp.append(ActionRecord('scene-year', year))
    tmp.append(ActionRecord('scene-date', date))
    tmp.append(ActionRecord('scene-time', time))
    tmp.append(ActionRecord('scene-start', ""))

    return tmp
