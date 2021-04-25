"""Action data create module."""

# Official Libraries


# My Modules
from stobu.core.instructioner import actions_data_apply_instructions
from stobu.elms.scenes import SceneItem
from stobu.syss import messages as msg
from stobu.tools.storydatareader import elm_title_of, scene_item_of, elm_data_of
from stobu.types.action import ActionsData, ActionRecord, ActType, ActDataType
from stobu.types.action import NORMAL_ACTIONS
from stobu.types.element import ElmType
from stobu.types.story import StoryData, StoryRecord
from stobu.utils import assertion
from stobu.utils.log import logger
from stobu.utils.strings import rid_rn, rid_head_space


__all__ = (
        'actions_data_from',
        )


# Define Constants
PROC = 'ACTION DATA CREATOR'


ACT_TYPE_TABLE = {
        ActType.BE: ('be',),
        ActType.COME: ('come',),
        ActType.DISCARD: ('discard',),
        ActType.DO: ('do',),
        ActType.DRAW: ('d', 'draw',),
        ActType.EXPLAIN: ('ex', 'explain',),
        ActType.FEEL: ('feel',),
        ActType.GO: ('go',),
        ActType.HAVE: ('have',),
        ActType.KNOW: ('know',),
        ActType.KNOWN: ('known',),
        ActType.OCCUR: ('occur',),
        ActType.PUT: ('put',),
        ActType.REMEMBER: ('rem', 'remember',),
        ActType.RID: ('rid',),
        ActType.TALK: ('t', 'talk',),
        ActType.THINK: ('think',),
        ActType.VOICE: ('voice',),
        ActType.SAME: ('-', 'same'),
        ActType.WEAR: ('wear',),
        }


TOP_LEVEL_ELMS = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ]


DATA_TITLE_TABLE = {
        ElmType.BOOK: ActDataType.BOOK_TITLE,
        ElmType.CHAPTER: ActDataType.CHAPTER_TITLE,
        ElmType.EPISODE: ActDataType.EPISODE_TITLE,
        ElmType.SCENE: ActDataType.SCENE_TITLE,
        }


LINE_EMPTY = ('', '\n', '\n\r', '\r\n')

LINE_COMMENT = '# '

LINE_HEAD = '## '

LINE_INSTRUCTION = '#! '

LINE_ACTION = '['


# Main
def actions_data_from(story_data: StoryData, tags: dict) -> ActionsData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    actions = conv_base_action_data_from(story_data)
    if not actions:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"base action data in {PROC}"))
        return None

    updated = update_actions_data_if_same(actions)
    if not updated or not updated.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"update action data in {PROC}"))
        return None

    applied = actions_data_apply_instructions(updated, tags)
    if not applied or not isinstance(applied, ActionsData) or not applied.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"apply action data in {PROC}"))
        return None

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return applied


def conv_base_action_data_from(story_data: StoryData) -> ActionsData:
    assert isinstance(story_data, StoryData)

    tmp = []

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if record.type in TOP_LEVEL_ELMS:
            tmp.append(_record_as_title_from(record))
        elif record.type is ElmType.SCENE:
            tmp.extend(_conv_action_records_on_scene_from(record))
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"element type in {PROC}"))
            continue

    return ActionsData(tmp)


def update_actions_data_if_same(actions_data: ActionsData) -> ActionsData:
    assert isinstance(actions_data, ActionsData)

    tmp = []
    cache = None

    for record in actions_data.get_data():
        assert isinstance(record, ActionRecord)
        if record.type in [ActType.DATA, ActType.NONE]:
            tmp.append(record)
        elif record.type in NORMAL_ACTIONS + [ActType.SAME,]:
            ret = _copy_action_record_if_same(record, cache)
            if ret:
                tmp.append(ret)
                cache = ret
        else:
            logger.warning(msg.ERR_FAIL_UNKNOWN_DATA.format(data=f"act type in {PROC}"))
            continue

    return ActionsData(tmp)


# Private Functions
def _act_type_from(action: str) -> ActType:
    assert isinstance(action, str)

    for act, check in ACT_TYPE_TABLE.items():
        if action in check:
            return act
    return ActType.NONE


def _conv_action_record_from(line: str) -> ActionRecord:
    assert isinstance(line, str)

    record = rid_rn(line)

    if record in LINE_EMPTY:
        return None
    elif record.startswith(LINE_COMMENT):
        return _record_as_comment_from(record)
    elif record.startswith(LINE_HEAD):
        return _record_as_head_from(record)
    elif record.startswith(LINE_INSTRUCTION):
        return _record_as_instruction_from(record)
    elif record.startswith(LINE_ACTION):
        return _record_as_action_from(record)
    elif record:
        return _record_as_text_from(record)
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"action line in {PROC}"))
        return None


def _conv_action_records_on_scene_from(record: StoryRecord) -> list:
    assert isinstance(record, StoryRecord)
    assert record.type is ElmType.SCENE

    tmp = []

    tmp.extend(_get_scene_head_info(record))
    tmp.append(_get_record_scene_start())

    for line in elm_data_of(record):
        assert isinstance(line, str)
        ret = _conv_action_record_from(line)
        if ret:
            assert isinstance(ret, ActionRecord)
            tmp.append(ret)

    tmp.append(_get_record_scene_end())

    return tmp


def _copy_action_record_if_same(record: ActionRecord, cache: ActionRecord) -> ActionRecord:
    assert isinstance(record, ActionRecord)

    if not cache:
        return record

    assert isinstance(cache, ActionRecord)

    act_type = cache.type if record.type is ActType.SAME else record.type
    sub_type = record.subtype
    subject = cache.subject if _is_same_mark(record.subject) else record.subject
    outline = cache.outline if _is_same_mark(record.outline) else record.outline
    desc = record.desc
    flags = record.flags
    note = record.note

    return ActionRecord(act_type, sub_type, subject, outline, desc, flags, note)


def _get_record_scene_end() -> ActionRecord:
    return ActionRecord(ActType.DATA, ActDataType.SCENE_END, '')


def _get_record_scene_start() -> ActionRecord:
    return ActionRecord(ActType.DATA, ActDataType.SCENE_START, '')


def _get_scene_head_info(record: StoryRecord) -> list:
    assert isinstance(record, StoryRecord)
    assert record.type is ElmType.SCENE

    tmp = []

    tmp.append(_record_as_title_from(record))
    tmp.append(_record_as_scene_camera_from(record))
    tmp.append(_record_as_scene_stage_from(record))
    tmp.append(_record_as_scene_year_from(record))
    tmp.append(_record_as_scene_date_from(record))
    tmp.append(_record_as_scene_time_from(record))

    return tmp


def _is_same_mark(text: str) -> bool:
    assert isinstance(text, str)

    return text in ('-', 'same')


def _record_as_action_from(line: str) -> ActionRecord:
    assert isinstance(line, str)

    tmp = line
    comment = ''
    if '# ' in line:
        tmp, comment = line.split('# ')
    cmd, desc = tmp[1:].split(']')
    subject, act, outline = cmd.split(':')
    return ActionRecord(
            _act_type_from(act),
            ActDataType.NONE,
            subject,
            outline,
            rid_head_space(desc),
            note=comment)


def _record_as_comment_from(line: str) -> ActionRecord:
    assert isinstance(line, str)

    comment = line.replace('# ', '')
    return ActionRecord(
            ActType.DATA,
            ActDataType.COMMENT,
            comment)


def _record_as_head_from(line: str) -> ActionRecord:
    assert isinstance(line, str)

    title = line.replace('## ', '')
    return ActionRecord(
            ActType.DATA,
            ActDataType.SCENE_HEAD,
            title)


def _record_as_instruction_from(line: str) -> ActionRecord:
    assert isinstance(line, str)

    tmp = line.replace('#! ', '')
    instruction = tmp
    outline = ''
    if ' ' in tmp:
        instruction, outline = tmp.split(' ')

    return ActionRecord(
            ActType.DATA,
            ActDataType.INSTRUCTION,
            instruction,
            outline)


def _record_as_scene_camera_from(record: StoryRecord) -> ActionRecord:
    assert isinstance(record, StoryRecord)
    return ActionRecord(
            ActType.DATA,
            ActDataType.SCENE_CAMERA,
            scene_item_of(record, SceneItem.CAMERA))


def _record_as_scene_date_from(record: StoryRecord) -> ActionRecord:
    assert isinstance(record, StoryRecord)
    return ActionRecord(
            ActType.DATA,
            ActDataType.SCENE_DATE,
            scene_item_of(record, SceneItem.DATE))


def _record_as_scene_stage_from(record: StoryRecord) -> ActionRecord:
    assert isinstance(record, StoryRecord)
    return ActionRecord(
            ActType.DATA,
            ActDataType.SCENE_STAGE,
            scene_item_of(record, SceneItem.STAGE))


def _record_as_scene_time_from(record: StoryRecord) -> ActionRecord:
    assert isinstance(record, StoryRecord)
    return ActionRecord(
            ActType.DATA,
            ActDataType.SCENE_TIME,
            scene_item_of(record, SceneItem.TIME))


def _record_as_scene_year_from(record: StoryRecord) -> ActionRecord:
    assert isinstance(record, StoryRecord)
    return ActionRecord(
            ActType.DATA,
            ActDataType.SCENE_YEAR,
            scene_item_of(record, SceneItem.YEAR))


def _record_as_text_from(line: str) -> ActionRecord:
    assert isinstance(line, str)

    return ActionRecord(
            ActType.DO,
            ActDataType.TEXT,
            '',
            rid_head_space(line),
            rid_head_space(line))


def _record_as_title_from(record: StoryRecord) -> ActionRecord:
    assert isinstance(record, StoryRecord)

    elm = assertion.is_instance(record.type, ElmType)

    # NOTE: ここは他にも何か情報入れる場合、追加
    return ActionRecord(
            ActType.DATA,
            DATA_TITLE_TABLE[elm],
            elm_title_of(record),
            )
