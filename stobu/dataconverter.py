"""Data convert module for storybuilder's data."""


# Official Libraries
from typing import Union
import re
import yaml


# My Modules
from stobu.datatypes import ActionData, ActionRecord
from stobu.datatypes import StoryRecord, StoryCode
from stobu.util.dicts import dict_sorted
from stobu.util.filepath import basename_of


__all__ = (
        'conv_action_record_from_scene_action',
        'conv_text_from_tag',
        'conv_text_in_action_data_by_tags',
        'conv_text_list_by_tags',
        'conv_to_dumpdata_of_yaml',
        'conv_to_story_record',
        )


# Main Functions
def conv_action_record_from_scene_action(actline: str) -> Union[ActionRecord, None]:
    assert isinstance(actline, str)

    _line = actline.rstrip('\n\r')
    assert isinstance(_line, str)
    if _line in ('', '\n', '\n\r'):
        # empty line
        return None
    elif _line.startswith('# '):
        # comment
        return ActionRecord('comment', _line)
    elif _line.startswith('## '):
        # head
        return ActionRecord('head-title', _line)
    elif _line.startswith('#!'):
        # instruction
        cmd = _line[2:]
        if ' ' in cmd:
            _cmd, txt = cmd.split(' ')
            return ActionRecord('instruction', "", _cmd, txt)
        else:
            return ActionRecord('instruction', "", cmd)
    elif _line.startswith('['):
        # action
        tmp = _line
        comment = ""
        if '# ' in _line:
            # exists comment
            _, comment = _line.split('# ')
            tmp = _
        inst, text = tmp[1:].split(']')
        subject, act, outline = inst.split(':')
        return ActionRecord("action", subject, act, outline, text, [], comment)
    elif _line:
        return ActionRecord("text", "", "do", "", _line)
    else:
        return None


def conv_code_from_action_record(record: ActionRecord,
        is_script_mode: bool = False) -> Union[StoryCode, None]:
    assert isinstance(record, ActionRecord)
    assert isinstance(is_script_mode, bool)

    if 'title' in record.type:
        return StoryCode(record.type, record.outline, record.note)
    elif record.type in ('scene-camera', 'scene-stage', 'scene-year', 'scene-date', 'scene-time'):
        return StoryCode(record.type, record.subject, record.note)
    elif record.type in ('scene-start', 'scene-end'):
        return StoryCode(record.type, "")
    elif 'action' == record.type:
        body = record.outline if is_script_mode else record.desc
        if 'talk' == record.action:
            if not is_script_mode:
                body = record.desc if record.desc else record.outline
            if body:
                return StoryCode('dialogue', body, record.subject)
            else:
                return None
        elif 'think' == record.action:
            return StoryCode('monologue', body, record.subject)
        elif body:
            return StoryCode('description', body, record.subject)
        else:
            return None
    elif 'text' == record.type:
        if record.desc:
            return StoryCode('description', record.desc, record.note)
        else:
            return None
    elif 'br' == record.type:
        return StoryCode(record.type, '')
    elif 'indent' == record.type:
        return StoryCode(record.type, '')
    return None


def conv_text_from_tag(text: str, tags: dict, prefix: str = '$') -> str:
    assert isinstance(text, str)
    assert isinstance(tags, dict)
    assert isinstance(prefix, str)

    tmp = text

    for key, val in tags.items():
        if prefix in tmp:
            tag_key = f"{prefix}{key}"
            if tag_key in tmp:
                if prefix:
                    tmp = re.sub(r'\{}{}'.format(prefix, key), val, tmp)
                else:
                    tmp = re.sub(key, val, tmp)
    return tmp


def conv_text_in_action_data_by_tags(action_data: ActionData,
        callings: dict, prefix: str = '$') -> ActionData:
    assert isinstance(action_data, ActionData)
    assert isinstance(callings, dict)
    assert isinstance(prefix, str)

    tmp = []

    for record in action_data.get_data():
        assert isinstance(record, ActionRecord)
        if record.type == 'action':
            if record.subject in callings:
                calling = callings[record.subject]
                calling['S'] = f"{record.subject}"
                calling['M'] = calling['me'] if 'me' in calling else '私'
                _calling = dict_sorted(calling, True)
                tmp.append(ActionRecord(
                    record.type,
                    record.subject,
                    record.action,
                    conv_text_from_tag(record.outline, _calling, prefix),
                    conv_text_from_tag(record.desc, _calling, prefix),
                    record.flags,
                    conv_text_from_tag(record.note, _calling, prefix),
                    ))
            else:
                tmp.append(record)
        else:
            tmp.append(record)
    return ActionData(tmp)


def conv_text_list_by_tags(textlist: list, tags: dict) -> list:
    assert isinstance(textlist, list)
    assert isinstance(tags, dict)

    tmp = []
    for text in textlist:
        tmp.append(conv_text_from_tag(text, tags))
    return tmp


def conv_to_dumpdata_of_yaml(data: dict) -> str:
    """Convert string data from yaml dict types."""
    assert isinstance(data, dict)

    tmp = yaml.safe_dump(data, default_flow_style=False)
    return rid_null_status(tmp)


def conv_to_story_record(ordername: str, orderdata: dict) -> StoryRecord:
    """Convert story record from order data."""
    assert isinstance(ordername, str)
    assert isinstance(orderdata, dict)
    assert '/' in ordername

    return StoryRecord(
            _get_category(ordername),
            basename_of(ordername),
            orderdata)


def rid_null_status(text: str) -> str:
    """Rid null from text."""
    assert isinstance(text, str)

    return text.replace('null', '')


# Private Functions
def _get_category(filename: str) -> str:
    assert isinstance(filename, str)

    category, fname = filename.split('/')
    return category
