"""Action data create module for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.dataconverter import conv_action_record_from_scene_action
from storybuilder.datatypes import ActionData, ActionRecord
from storybuilder.datatypes import StoryData, StoryRecord
from storybuilder.util.log import logger


__all__ = (
        'get_action_data',
        )


# Main Function
def get_action_data(story_data: StoryData) -> ActionData:
    assert isinstance(story_data, StoryData)
    logger.debug("Creating Action data from story data...")

    tmp = []

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if record.category == 'book':
            tmp.append(ActionRecord('book-title', "", "", record.data['title']))
        elif record.category == 'chapter':
            tmp.append(ActionRecord('chapter-title', "", "", record.data['title']))
        elif record.category == 'episode':
            tmp.append(ActionRecord('episode-title', "", "", record.data['title']))
        elif record.category == 'scene':
            ret = _get_action_data_in_scene(record)
            if ret:
                tmp.extend(ret)
        else:
            logger.debug("Unknown StoryRecord data!: %s", record)
            continue

    logger.debug("...Succeeded create Action data.")
    return ActionData(tmp)


# Private Functions
def _get_action_data_in_scene(record: StoryRecord) -> list:
    assert isinstance(record, StoryRecord)
    assert record.category == 'scene'

    tmp = []

    tmp.append(ActionRecord('scene-title', "", "", record.data['title']))
    tmp.append(ActionRecord('scene-camera', record.data['camera'], ""))
    tmp.append(ActionRecord('scene-stage', record.data['stage']))
    tmp.append(ActionRecord('scene-year', record.data['year']))
    tmp.append(ActionRecord('scene-date', record.data['date']))
    tmp.append(ActionRecord('scene-time', record.data['time']))
    tmp.append(ActionRecord('scene-start', ""))

    for line in record.data['markdown']:
        assert isinstance(line, str)
        ret = conv_action_record_from_scene_action(line)
        if ret:
            assert isinstance(ret, ActionRecord)
            tmp.append(ret)

    tmp.append(ActionRecord('scene-end', ""))

    return tmp


