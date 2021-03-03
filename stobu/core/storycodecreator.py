"""Story code create module for storybuilder project."""


# Official Libraries


# My Modules
from stobu.dataconverter import conv_code_from_action_record
from stobu.datatypes import ActionData, ActionRecord
from stobu.datatypes import StoryCodeData
from stobu.util.log import logger


__all__ = (
        'get_story_code_data',
        )


# Main Function
def get_story_code_data(action_data: ActionData, is_script_mode: bool) -> StoryCodeData:
    assert isinstance(action_data, ActionData)
    assert isinstance(is_script_mode, bool)

    tmp = []
    for record in action_data.get_data():
        assert isinstance(record, ActionRecord)
        ret = conv_code_from_action_record(record, is_script_mode)
        if ret:
            tmp.append(ret)

    return StoryCodeData(tmp)
