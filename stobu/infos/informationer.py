"""Information creator module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.formats.info import format_infos_data
from stobu.infos.fashioninfos import fashion_infos_from
from stobu.infos.flaginfos import flag_infos_from
from stobu.infos.personinfos import person_infos_from
from stobu.infos.transitions import scene_transition_data_from
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_text_list, translate_tags_str
from stobu.types.action import ActDataType, ActionRecord, ActionsData, ActType
from stobu.types.action import TITLE_ACTIONS, NORMAL_ACTIONS
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import SceneInfo
from stobu.types.output import OutputsData
from stobu.utils import assertion
from stobu.utils.dicts import dict_sorted
from stobu.utils.log import logger


__all__ = (
        'infos_data_from',
        'outputs_data_from_infos_data',
        )


# Define Constants
PROC = 'INFORAMATIONER'


# Main
def infos_data_from(actions_data: ActionsData, tags: dict) -> InfosData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    base_data = _base_data_from(actions_data)

    updated = update_data_tags(base_data, tags)

    transitions = scene_transition_data_from(updated)

    flags = flag_infos_from(updated)

    persons = person_infos_from(updated)

    fashions = fashion_infos_from(updated)

    data_set = transitions + flags + persons + fashions

    eliminated = _eliminate_empty_records(data_set)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return eliminated


def outputs_data_from_infos_data(infos_data: InfosData, tags: dict,
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


def update_data_tags(origin_data: list, tags: dict) -> InfosData:
    assert isinstance(origin_data, list)
    assert isinstance(tags, dict)

    _PROC = f"{PROC}: update tags"
    logger.debug(msg.PROC_START.format(proc=_PROC))

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

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return InfosData(tmp)


# Private Functions
def _base_data_from(actions_data: ActionsData) -> list:
    assert isinstance(actions_data, ActionsData)

    _PROC = f"{PROC}: base data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

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

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


def _eliminate_empty_records(base_data: InfosData) -> InfosData:
    assert isinstance(base_data, InfosData)

    tmp = []

    for record in base_data.get_data():
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

    return InfosData(tmp)


def _get_record_as_scene_end() -> InfoRecord:
    return InfoRecord(InfoType.SCENE_END, ActType.DATA, '', '', '')


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
