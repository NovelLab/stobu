"""Scene info collection module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.formats.info import format_infos_data
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_text_list, translate_tags_str
from stobu.types.action import ActDataType, ActionRecord, ActionsData, ActType
from stobu.types.action import NORMAL_ACTIONS, TITLE_ACTIONS
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import SceneInfo
from stobu.types.info import FlagInfo, FlagType
from stobu.types.output import OutputsData
from stobu.utils import assertion
from stobu.utils.dicts import dict_sorted
from stobu.utils.log import logger


__all__ = (
        'sceneinfos_data_from',
        'outputs_data_from_sceneinfos_data',
        )


# Define Constants
PROC = 'SCENE INFO COLLECTOR'


# Main
def sceneinfos_data_from(actions_data: ActionsData, tags: dict) -> InfosData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    base_data = _base_info_data_from(actions_data)

    updated = update_data_tags(base_data, tags)

    transition = _conv_scene_transition_data_from(updated)

    flag_info = _conv_scene_flags_data_from(updated)

    data_set = transition + flag_info

    eliminated = _eliminate_empty_records(data_set)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return InfosData(eliminated)


def outputs_data_from_sceneinfos_data(infos_data: InfosData, tags: dict,
        is_comment: bool = False) -> OutputsData:
    assert isinstance(infos_data, InfosData)
    assert isinstance(tags, dict)
    assert isinstance(is_comment, bool)

    _PROC = f"{PROC}: convert outputs data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    formatted = format_infos_data(infos_data, is_comment)

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


def update_data_tags(origin_data: list, tags: dict) -> list:
    assert isinstance(origin_data, list)
    assert isinstance(tags, dict)

    tmp = []
    callings = get_calling_tags()

    for record in origin_data:
        assert isinstance(record, InfoRecord)
        if record.type is InfoType.ACTION:
            tmp.append(_update_tags_action_record(record, tags, callings))
        elif InfoType.SCENE_HEAD is record.type:
            tmp.append(_update_tags_scene_head_record(record, tags))
        else:
            tmp.append(record)

    return tmp


# Private Functions
def _base_info_data_from(actions_data: ActionsData) -> list:
    assert isinstance(actions_data, ActionsData)

    tmp = []
    cache = SceneInfo()

    for record in actions_data.get_data():
        assert isinstance(record, ActionRecord)
        if ActType.DATA is record.type:
            if record.subtype in TITLE_ACTIONS:
                tmp.append(_record_as_title_from(record))
            elif ActDataType.SCENE_CAMERA is record.subtype:
                cache.camera = record.subject
            elif ActDataType.SCENE_STAGE is record.subtype:
                cache.stage = record.subject
            elif ActDataType.SCENE_YEAR is record.subtype:
                cache.year = record.subject
            elif ActDataType.SCENE_DATE is record.subtype:
                cache.date = record.subject
            elif ActDataType.SCENE_TIME is record.subtype:
                cache.time = record.subject
            elif ActDataType.SCENE_START is record.subtype:
                tmp.append(_record_as_scene_head_from(cache.cloned()))
            elif ActDataType.SCENE_END is record.subtype:
                tmp.append(_get_record_as_scene_end())
                cache.reset()
            elif ActDataType.COMMENT is record.subtype:
                tmp.append(_record_as_comment_from(record))
            elif ActDataType.FORESHADOW is record.subtype:
                tmp.append(_record_as_foreshadow_from(record))
            elif ActDataType.PAYOFF is record.subtype:
                tmp.append(_record_as_payoff_from(record))
            elif record.subtype in [ActDataType.BR,
                    ActDataType.PARAGRAPH_START,
                    ActDataType.PARAGRAPH_END,
                    ActDataType.INSTRUCTION]:
                continue
            elif ActDataType.TEXT is record.subtype:
                continue
            else:
                logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"act data type in {PROC}"))
                continue
        elif record.type in NORMAL_ACTIONS:
            tmp.append(_record_as_action_from(record))
        elif ActType.NONE is record.type:
            continue
        elif ActType.SAME is record.type:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"same act type in {PROC}"))
            continue
        else:
            continue

    return tmp


def _conv_scene_flags_data_from(base_data: list) -> InfosData:
    assert isinstance(base_data, list)

    _PROC = f"{PROC}: flag data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    index = 0

    tmp.append(_get_record_as_splitter())
    tmp.append(InfoRecord(
        InfoType.DATA_TITLE, ActType.DATA, '## SCENE FLAG INFOS', '', ''))

    for record in base_data:
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            continue
        elif InfoType.FLAG_FORESHADOW is record.type:
            tmp.append(_record_as_flag_info_from(record, index, FlagType.FLAG))
        elif InfoType.FLAG_PAYOFF is record.type:
            tmp.append(_record_as_flag_info_from(record, index, FlagType.DEFLAG))
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_flag_info_split())
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


def _conv_scene_transition_data_from(base_data: list) -> InfosData:
    assert isinstance(base_data, list)

    _PROC = f"{PROC}: scene transition"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    cache = SceneInfo()

    tmp.append(_get_record_as_splitter())
    tmp.append(InfoRecord(
        InfoType.DATA_TITLE, ActType.DATA, '## SCENE TRANSITIONS', '', ''))

    for record in base_data:
        assert isinstance(record, InfoRecord)
        if InfoType.SCENE_HEAD is record.type:
            tmp.append(_record_of_scene_transition_from(record, cache))
            tmp.append(
                    InfoRecord(InfoType.SCENE_TRANSITION, record.act,
                        record.subject, record.outline, record.note))
            cache = record.note
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_transition_split())
        elif InfoType.TITLE_SCENE is record.type:
            continue
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


def _eliminate_empty_records(base_data: list) -> list:
    assert isinstance(base_data, list)

    tmp = []

    for record in base_data:
        assert isinstance(record, InfoRecord)
        if record.type in [InfoType.COMMENT,]:
            if InfoType.COMMENT is record.type:
                if record.subject:
                    tmp.append(record)
            else:
                if record.outline:
                    tmp.append(record)
        else:
            tmp.append(record)

    return tmp


def _get_record_as_flag_info_split() -> InfoRecord:
    info = FlagInfo(FlagType.NONE, 0, '', '', '')

    return InfoRecord(InfoType.FLAG_INFO, ActType.DATA, '', '', info)


def _get_record_as_scene_end() -> InfoRecord:
    return InfoRecord(InfoType.SCENE_END, ActType.DATA, '', '', '')


def _get_record_as_splitter() -> InfoRecord:
    return InfoRecord(InfoType.SPLITTER, ActType.DATA, '', '', '')


def _get_record_as_transition_split() -> InfoRecord:
    line = '---'
    info = SceneInfo(line, line, line, line, line)

    return InfoRecord(InfoType.SCENE_TRANSITION, ActType.DATA, '', '', info)


def _record_as_action_from(record: ActionRecord) -> InfoRecord:
    return InfoRecord(
            InfoType.ACTION,
            record.type,
            record.subject,
            record.outline,
            record.note)


def _record_as_comment_from(record: ActionRecord) -> InfoRecord:
    assert isinstance(record, ActionRecord)

    return InfoRecord(
            InfoType.COMMENT,
            ActType.DATA,
            record.subject,
            record.outline,
            record.note)


def _record_as_flag_info_from(record: InfoRecord, index: int,
        flag_type: FlagType) -> InfoRecord:
    assert isinstance(record, InfoRecord)
    assert isinstance(index, int)
    assert isinstance(flag_type, FlagType)

    return InfoRecord(
            InfoType.FLAG_INFO,
            ActType.DATA,
            '', '',
            FlagInfo(flag_type, index, record.subject, record.outline, record.note))


def _record_as_foreshadow_from(record: ActionRecord) -> InfoRecord:
    assert isinstance(record, ActionRecord)

    return InfoRecord(
            InfoType.FLAG_FORESHADOW,
            ActType.DATA,
            record.subject,
            record.outline,
            record.note)


def _record_as_payoff_from(record: ActionRecord) -> InfoRecord:
    assert isinstance(record, ActionRecord)

    return InfoRecord(
            InfoType.FLAG_PAYOFF,
            ActType.DATA,
            record.subject,
            record.outline,
            record.note)


def _record_as_scene_head_from(sceneinfo: SceneInfo) -> InfoRecord:
    assert isinstance(sceneinfo, SceneInfo)

    return InfoRecord(InfoType.SCENE_HEAD, ActType.DATA, '', '', sceneinfo)


def _record_as_title_from(record: ActionRecord) -> InfoRecord:
    assert isinstance(record, ActionRecord)

    return InfoRecord(
            _title_from(record),
            ActType.DATA,
            record.subject,
            record.outline,
            record.note)


def _record_of_scene_transition_from(record: InfoRecord,
        cache: SceneInfo) -> InfoRecord:
    assert isinstance(record, InfoRecord)
    assert isinstance(cache, SceneInfo)

    def _diff(a: str, b: str) -> str:
        if a != b:
            return '↓'
        else:
            return '…'

    base = assertion.is_instance(record.note, SceneInfo)

    dif = SceneInfo()

    dif.camera = _diff(base.camera, cache.camera)
    dif.stage = _diff(base.stage, cache.stage)
    dif.year = _diff(base.year, cache.year)
    dif.date = _diff(base.date, cache.date)
    dif.time = _diff(base.time, cache.time)

    return InfoRecord(InfoType.SCENE_TRANSITION, ActType.DATA, '', '', dif)


def _title_from(record: ActionRecord) -> InfoType:
    assert isinstance(record, ActionRecord)

    if ActDataType.BOOK_TITLE is record.subtype:
        return InfoType.TITLE_BOOK
    elif ActDataType.CHAPTER_TITLE is record.subtype:
        return InfoType.TITLE_CHAPTER
    elif ActDataType.EPISODE_TITLE is record.subtype:
        return InfoType.TITLE_EPISODE
    elif ActDataType.SCENE_TITLE is record.subtype:
        return InfoType.TITLE_SCENE
    elif ActDataType.SCENE_HEAD is record.subtype:
        return InfoType.TITLE_TEXT
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"title data type in {PROC}"))
        return InfoType.NONE


def _update_tags_action_record(record: InfoRecord, tags: dict,
        callings: dict) -> InfoRecord:
    assert isinstance(record, InfoRecord)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)

    if record.subject in callings:
        calling = dict_sorted(callings[record.subject], True)
        return InfoRecord(
            record.type,
            record.act,
            translate_tags_str(record.subject, tags, True, None),
            translate_tags_str(record.outline, calling),
            translate_tags_str(record.note, calling),
            )
    else:
        return InfoRecord(
                record.type,
                record.act,
                translate_tags_str(record.subject, tags, True, None),
                record.outline,
                record.note,
                )


def _update_tags_scene_head_record(record: InfoRecord, tags: dict) -> InfoRecord:
    assert isinstance(record, InfoRecord)
    assert isinstance(tags, dict)

    info = assertion.is_instance(record.note, SceneInfo)
    _info = SceneInfo()
    _info.camera = translate_tags_str(info.camera, tags, True, None)
    _info.stage = translate_tags_str(info.stage, tags, True, None)
    _info.year = translate_tags_str(str(info.year), tags, True, None)
    _info.date = translate_tags_str(str(info.date), tags, True, None)
    _info.time = translate_tags_str(str(info.time), tags, True, None)

    return InfoRecord(
            record.type,
            record.act,
            record.subject,
            record.outline,
            _info)
