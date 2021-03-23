"""Build script module for storybuilder project."""


# Official Libraries


# My Modules
from stobu.core.actiondatacreator import get_action_data
from stobu.core.contentscreator import get_contents_list
from stobu.core.instructions import apply_instruction_to_action_data
from stobu.core.rubibuilder import apply_rubi_convert
from stobu.core.storycodecreator import get_story_code_data
from stobu.dataconverter import conv_text_in_action_data_by_tags, conv_text_list_by_tags
from stobu.datatypes import ActionData
from stobu.datatypes import OutputData
from stobu.datatypes import StoryCodeData
from stobu.datatypes import StoryData
from stobu.formatter import format_contents_table_data, format_script_data, get_breakline
from stobu.nametagmanager import NameTagDB
from stobu.util import assertion
from stobu.util.log import logger


__all__ = (
        'on_build_script',
        'get_story_code_data_from_story_data_as_script',
        )


# Main Function
def on_build_script(story_data: StoryData, tags: dict, is_rubi: bool) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(is_rubi, bool)

    contents = get_contents_list(story_data)

    story_code_data = assertion.is_instance(
            get_story_code_data_from_story_data_as_script(story_data, tags), StoryCodeData)

    scripts = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_script_data(story_code_data, tags)

    output_data = conv_text_list_by_tags(scripts, tags)

    return OutputData(
            apply_rubi_convert(output_data) if is_rubi else output_data)


# Functions
def get_story_code_data_from_story_data_as_script(story_data: StoryData, tags: dict) -> StoryCodeData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    action_data = assertion.is_instance(get_action_data(story_data), ActionData)

    action_data_applied = assertion.is_instance(
            apply_instruction_to_action_data(action_data, True), ActionData)

    callings = NameTagDB.get_calling_tags()
    action_data_tagfixed = assertion.is_instance(
            conv_text_in_action_data_by_tags(action_data_applied, tags, callings),
            ActionData)

    story_code_data = assertion.is_instance(get_story_code_data(action_data_tagfixed, True),
            StoryCodeData)

    return story_code_data
