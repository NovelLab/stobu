"""Build Struct module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.formats.common import get_breakline
from stobu.formats.struct import format_structs_data
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_text_list, translate_tags_str
from stobu.types.action import ActionsData, ActionRecord, ActDataType, ActType
from stobu.types.action import NORMAL_ACTIONS, TITLE_ACTIONS
from stobu.types.element import ElmType
from stobu.types.info import SceneInfo
from stobu.types.output import OutputsData
from stobu.types.struct import StructRecord, StructsData, StructType
from stobu.types.struct import STRUCT_TITLES
from stobu.types.struct import SceneDataInfo, DataInfoType
from stobu.utils import assertion
from stobu.utils.dicts import dict_sorted
from stobu.utils.log import logger
from stobu.utils.strings import just_string_of


__all__ = (
        'structs_data_from',
        'outputs_data_from_structs_data',
        )


# Define Constants
PROC = 'BUILD STRUCT'


# Main
def structs_data_from(actions_data: ActionsData, tags: dict) -> StructsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    base_data = _base_structs_data_from(actions_data)

    updated = update_data_tags(base_data, tags)

    data_updated = update_scene_info(updated)

    eliminated = _eliminate_empty_records(data_updated)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return StructsData(eliminated)


def outputs_data_from_structs_data(structs_data: StructsData, tags: dict,
        is_comment: bool = False) -> OutputsData:
    assert isinstance(structs_data, StructsData)
    assert isinstance(tags, dict)
    assert isinstance(is_comment, bool)

    _PROC = f"{PROC}: convert outputs data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    formatted = format_structs_data(structs_data, is_comment)

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


def update_data_tags(origin_data: list, tags: dict) -> list:
    assert isinstance(origin_data, list)
    assert isinstance(tags, dict)

    tmp = []
    callings = get_calling_tags()

    for record in origin_data:
        assert isinstance(record, StructRecord)
        if record.type is StructType.ACTION:
            tmp.append(_update_tags_action_record(record, tags, callings))
        elif StructType.SCENE_DATA is record.type:
            tmp.append(_update_tags_scene_data_record(record, tags))
        else:
            tmp.append(record)

    return tmp


def update_scene_info(base_data: list) -> list:
    assert isinstance(base_data, list)

    _PROC = f"{PROC}: update scene info"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    actions = []

    person_data = SceneDataInfo(DataInfoType.PERSON)
    item_data = SceneDataInfo(DataInfoType.ITEM)
    event_data = SceneDataInfo(DataInfoType.EVENT)

    def _data_reset():
        person_data.reset()
        item_data.reset()
        event_data.reset()

    for record in base_data:
        assert isinstance(record, StructRecord)
        if StructType.ACTION is record.type:
            actions.append(record)
            if ActType.BE is record.act:
                if record.subject:
                    person_data.append(record.subject)
            elif ActType.COME is record.act:
                if record.subject:
                    person_data.append(f"IN {record.subject}")
            elif ActType.GO is record.act:
                if record.subject:
                    person_data.append(f"OUT {record.subject}")
            elif ActType.HAVE is record.act:
                if record.subject and record.outline:
                    item_data.append(f"IN {record.outline}")
                elif record.subject:
                    item_data.append(f"IN {record.subject}")
            elif ActType.DISCARD is record.act:
                if record.subject and record.outline:
                    item_data.append(f"OUT {record.outline}")
                elif record.subject:
                    item_data.append(f"OUT {record.subject}")
            elif ActType.PUT is record.act:
                if record.subject:
                    item_data.append(record.subject)
            elif ActType.RID is record.act:
                if record.subject:
                    item_data.append(f"RM {record.subject}")
            elif ActType.OCCUR is record.act:
                if record.subject:
                    event_data.append(record.subject)
        elif StructType.SCENE_DATA is record.type:
            tmp.append(record)
        elif StructType.SCENE_END is record.type:
            tmp.append(_record_as_data_info_from(person_data.cloned()))
            tmp.append(_record_as_data_info_from(item_data.cloned()))
            tmp.append(_record_as_data_info_from(event_data.cloned()))
            _data_reset()
            tmp.extend(actions)
            tmp.append(record)
            actions = []
        elif record.type in STRUCT_TITLES:
            tmp.append(record)
        else:
            tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


# Private Functions
def _base_structs_data_from(actions_data: ActionsData) -> list:
    assert isinstance(actions_data, ActionsData)

    tmp = []
    cache = SceneInfo()

    for record in actions_data.get_data():
        assert isinstance(record, ActionRecord)
        if record.type is ActType.DATA:
            if record.subtype in TITLE_ACTIONS:
                tmp.append(_record_as_title_from(record))
            elif ActDataType.SCENE_START is record.subtype:
                tmp.append(_record_as_scene_data_from(cache))
            elif ActDataType.SCENE_END is record.subtype:
                tmp.append(_get_record_as_scene_end())
                cache.reset()
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
            elif ActDataType.COMMENT is record.subtype:
                tmp.append(_record_as_comment_from(record))
            elif ActDataType.TEXT is record.subtype:
                tmp.append(_record_as_text_from(record))
            elif record.subtype in [ActDataType.BR,
                    ActDataType.FORESHADOW, ActDataType.PAYOFF,
                    ActDataType.PARAGRAPH_START, ActDataType.PARAGRAPH_END,]:
                continue
            else:
                logger.warning(msg.ERR_FAIL_UNKNOWN_DATA.format(data=f"act data sub type in {PROC}"))
                continue
        elif record.type in NORMAL_ACTIONS:
            tmp.append(_record_as_action_from(record))
        elif record.type in [ActType.NONE, ActType.SAME]:
            # NOTE: SE?
            continue
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"act type in {PROC}"))
            continue

    return tmp


def _eliminate_empty_records(base_data: list) -> list:
    assert isinstance(base_data, list)

    tmp = []

    for record in base_data:
        assert isinstance(record, StructRecord)
        if record.type in [StructType.COMMENT, StructType.TEXT]:
            if StructType.COMMENT is record.type:
                if record.subject:
                    tmp.append(record)
            elif StructType.TEXT is record.type:
                if record.subject:
                    tmp.append(record)
            else:
                if record.desc:
                    tmp.append(record)
        else:
            tmp.append(record)

    return tmp


def _get_record_as_scene_end() -> StructRecord:
    return StructRecord(StructType.SCENE_END, ActType.NONE, '', '', '')


def _record_as_action_from(record: ActionRecord) -> StructRecord:
    assert isinstance(record, ActionRecord)

    return StructRecord(
            StructType.ACTION,
            record.type, record.subject, record.outline, record.note)


def _record_as_comment_from(record: ActionRecord) -> StructRecord:
    assert isinstance(record, ActionRecord)

    return StructRecord(
            StructType.COMMENT,
            ActType.DATA, record.subject, record.outline, record.note)


def _record_as_data_info_from(info: SceneDataInfo) -> StructRecord:
    assert isinstance(info, SceneDataInfo)

    type = StructType.NONE

    if DataInfoType.PERSON is info.type:
        type = StructType.PERSON_DATA
    elif DataInfoType.ITEM is info.type:
        type = StructType.ITEM_DATA
    elif DataInfoType.EVENT is info.type:
        type = StructType.EVENT_DATA

    return StructRecord(type, ActType.DATA, '', '', info)


def _record_as_scene_data_from(info: SceneInfo) -> StructRecord:
    assert isinstance(info, SceneInfo)

    return StructRecord(
            StructType.SCENE_DATA, ActType.DATA, info.camera, info.stage, info.cloned())


def _record_as_text_from(record: ActionRecord) -> StructRecord:
    assert isinstance(record, ActionRecord)

    return StructRecord(
            StructType.TEXT,
            ActType.DO, record.subject, record.outline, record.note)


def _record_as_title_from(record: ActionRecord) -> StructRecord:
    assert isinstance(record, ActionRecord)

    return StructRecord(
            _title_type_of(record),
            ActType.DATA, record.subject, record.outline, record.note)


def _title_type_of(record: ActionRecord) -> StructType:
    assert isinstance(record, ActionRecord)

    if ActDataType.BOOK_TITLE is record.subtype:
        return StructType.TITLE_BOOK
    elif ActDataType.CHAPTER_TITLE is record.subtype:
        return StructType.TITLE_CHAPTER
    elif ActDataType.EPISODE_TITLE is record.subtype:
        return StructType.TITLE_EPISODE
    elif ActDataType.SCENE_TITLE is record.subtype:
        return StructType.TITLE_SCENE
    elif ActDataType.SCENE_HEAD is record.subtype:
        return StructType.TITLE_TEXT
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"title type in {PROC}"))
        return StructType.NONE


def _update_tags_action_record(record: StructRecord, tags: dict,
        callings: dict) -> StructRecord:
    assert isinstance(record, StructRecord)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)

    if record.subject in callings:
        calling = dict_sorted(callings[record.subject], True)
        return StructRecord(
            record.type,
            record.act,
            translate_tags_str(record.subject, tags, True, None),
            translate_tags_str(record.outline, calling),
            translate_tags_str(record.note, calling),
            )
    else:
        return StructRecord(
                record.type,
                record.act,
                translate_tags_str(record.subject, tags, True, None),
                record.outline,
                record.note,
                )


def _update_tags_scene_data_record(record: StructRecord, tags: dict) -> StructRecord:
    assert isinstance(record, StructRecord)
    assert isinstance(tags, dict)

    info = assertion.is_instance(record.note, SceneInfo)
    updated = SceneInfo()

    updated.camera = translate_tags_str(info.camera, tags, True, None)
    updated.stage = translate_tags_str(info.stage, tags, True, None)
    updated.year = translate_tags_str(str(info.year), tags, True, None)
    updated.date = translate_tags_str(str(info.date), tags, True, None)
    updated.time = translate_tags_str(str(info.time), tags, True, None)

    return StructRecord(
            record.type,
            record.act,
            translate_tags_str(record.subject, tags, True, None),
            translate_tags_str(record.outline, tags, True, None),
            updated)
