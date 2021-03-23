"""Building module for scene info."""


# Official Libraries
import copy


# My Modules
from stobu.core.actiondatacreator import get_action_data
from stobu.core.contentscreator import get_contents_list
from stobu.core.instructions import apply_instruction_to_action_data
from stobu.core.rubibuilder import apply_rubi_convert
from stobu.core.storycodecreator import get_story_code_data
from stobu.dataconverter import conv_text_in_action_data_by_tags, conv_text_list_by_tags
from stobu.datatypes import ActionData, ActionRecord
from stobu.datatypes import OutputData
from stobu.datatypes import StoryCodeData, StoryCode
from stobu.datatypes import StoryData
from stobu.formatter import format_contents_table_data, format_scene_info_data, get_breakline
from stobu.nametagmanager import NameTagDB
from stobu.util import assertion
from stobu.util.log import logger


__all__ = (
        'on_build_scene_info',
        )


# Main Functions
def on_build_scene_info(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    contents = get_contents_list(story_data)

    action_data = assertion.is_instance(get_action_data_tagfixed(story_data, tags),
            ActionData)

    story_code_data = assertion.is_instance(
            get_story_code_from_action_data(action_data), StoryCodeData)

    info_data = format_contents_table_data(contents) \
            + ['\n', get_breakline()] \
            + format_scene_info_data(story_code_data, tags)

    output_data = conv_text_list_by_tags(info_data, tags)

    return OutputData(output_data)


# Functions
def get_action_data_tagfixed(story_data: StoryData, tags: dict) -> ActionData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    action_data = assertion.is_instance(get_action_data(story_data), ActionData)

    action_data_applied = assertion.is_instance(
            apply_instruction_to_action_data(action_data), ActionData)

    callings = NameTagDB.get_calling_tags()
    action_data_tagfixed = assertion.is_instance(
            conv_text_in_action_data_by_tags(action_data, callings),
            ActionData)

    return action_data_tagfixed


def get_story_code_from_action_data(action_data: ActionData) -> StoryCodeData:
    assert isinstance(action_data, ActionData)

    tmp = []
    scene_data = {
            'camera': '',
            'stage': '',
            'year': '',
            'date': '',
            'time': '',
            }
    elapsed = {
            'camera': '',
            'stage': '',
            'year': '',
            'date': '',
            'time': '',
            }
    for record in action_data.get_data():
        assert isinstance(record, ActionRecord)

        if 'title' in record.type:
            tmp.append(StoryCode(record.type, record.outline, record.note))
        elif record.type in ('scene-camera', 'scene-stage', 'scene-year', 'scene-date', 'scene-time'):
            tmp.append(StoryCode(record.type, record.subject, record.note))
            if record.type == 'scene-camera':
                elapsed['camera'] = 'changed' if scene_data['camera'] != record.subject else ''
                scene_data['camera'] = record.subject
            elif record.type == 'scene-stage':
                elapsed['stage'] = 'changed' if scene_data['stage'] != record.subject else ''
                scene_data['stage'] = record.subject
            elif record.type == 'year':
                elapsed['year'] = 'changed' if scene_data['year'] != record.subject else ''
                scene_data['year'] = record.subject
            elif record.type == 'date':
                elapsed['date'] = 'changed' if scene_data['date'] != record.subject else ''
                scene_data['date'] = record.subject
            elif record.type == 'time':
                elapsed['time'] = 'changed' if scene_data['time'] != record.subject else ''
                scene_data['time'] = record.subject
            else:
                pass
        elif record.type in ('scene-start', 'scene-end'):
            if record.type == 'scene-end':
                tmp.append(StoryCode('scene-elapsed', '', copy.deepcopy(elapsed)))
            tmp.append(StoryCode(record.type, ""))
        elif 'action' == record.type:
            continue
        elif 'text' == record.type:
            continue
        elif 'br' == record.type:
            continue
        elif 'indent' == record.type:
            continue
        else:
            continue

    return StoryCodeData(tmp)
