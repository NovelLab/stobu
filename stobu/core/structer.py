"""Build Struct module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.formats.common import get_breakline
from stobu.formats.struct import format_structs_data
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_text_list, translate_tags_str
from stobu.types.action import ActionsData, ActionRecord, ActDataType, ActType
from stobu.types.action import NORMAL_ACTIONS
from stobu.types.element import ElmType
from stobu.types.output import OutputsData
from stobu.types.struct import StructRecord, StructsData, StructType
from stobu.utils.dicts import dict_sorted
from stobu.utils.log import logger
from stobu.utils.strings import just_string_of


__all__ = (
        'scene_transition_data_from',
        'structs_data_from',
        'outputs_data_from_structs_data',
        )


# Define Constants
PROC = 'BUILD STRUCT'


ACT_TITLES = [
        ActDataType.BOOK_TITLE,
        ActDataType.CHAPTER_TITLE,
        ActDataType.EPISODE_TITLE,
        ActDataType.SCENE_TITLE,
        ActDataType.SCENE_HEAD,
        ]


# Main
def scene_transition_data_from(structs_data: StructsData, tags: dict) -> OutputsData:
    assert isinstance(structs_data, StructsData)
    assert isinstance(tags, dict)

    _PROC = f"{PROC}: transtion data"
    logger.debug(msg.PROC_START.format(proc=_PROC))
    tmp = []
    cache = {
            'camera': '',
            'stage': '',
            'year': '',
            'date': '',
            'time': '',
            }
    tmp.append("# SCENE TRANSITIONS\n\n")

    for record in structs_data.get_data():
        assert isinstance(record, StructRecord)
        if StructType.SCENE_DATA is record.type:
            camera = record.subject
            stage = record.outline
            year = record.note['year']
            date = record.note['date']
            time = record.note['time']
            tmp.append(_format_transition_record_as_compare(
                camera, stage, year, date, time, cache))
            tmp.append("\n")
            tmp.append(_format_transition_record(camera, stage, year, date, time))
            tmp.append("\n")
            cache['camera'] = camera
            cache['stage'] = stage
            cache['year'] = year
            cache['date'] = date
            cache['time'] = time
        elif StructType.TITLE_EPISODE is record.type:
            line = '----'
            tmp.append(_format_transition_record(line, line, line, line, line))
            tmp.append("\n")

    tmp.append("\n")
    tmp.append(get_breakline())

    translated = translate_tags_text_list(tmp, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


def structs_data_from(actions_data: ActionsData, tags: dict) -> StructsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    base_data = _base_structs_data_from(actions_data)

    updated = update_data_tags(base_data, tags)

    updated_data = update_scene_data(updated)

    eliminated = _eliminate_empty_records(updated_data)

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


def update_scene_data(origin_data: list) -> list:
    assert isinstance(origin_data, list)

    tmp = []
    cache = {'person': [],
            'item': [],
            }
    def reset_cache():
        cache['person'] = []
        cache['item'] = []

    for record in origin_data:
        assert isinstance(record, StructRecord)
        if StructType.ACTION is record.type:
            tmp.append(record)
            if record.subject:
                cache['person'].append(record.subject)
        elif StructType.SCENE_DATA is record.type:
            tmp.append(record)
        elif StructType.SCENE_END is record.type:
            tmp.append(_conv_item_data_record(cache))
            reset_cache()
        else:
            tmp.append(record)

    return tmp


# Private Functions
def _base_structs_data_from(actions_data: ActionsData) -> list:
    assert isinstance(actions_data, ActionsData)

    tmp = []
    cache = {
            'camera': None,
            'stage': None,
            'year': None,
            'date': None,
            'time': None,
            }
    def reset_cache():
        cache['camera'] = None
        cache['stage'] = None
        cache['year'] = None
        cache['date'] = None
        cache['time'] = None

    for record in actions_data.get_data():
        assert isinstance(record, ActionRecord)
        if record.type is ActType.DATA:
            if record.subtype in ACT_TITLES:
                tmp.append(_record_as_title_from(record))
            elif ActDataType.SCENE_START is record.subtype:
                tmp.append(_record_as_scene_data_from(
                    cache['camera'], cache['stage'], cache['year'],
                    cache['date'], cache['time']))
            elif ActDataType.SCENE_END is record.subtype:
                tmp.append(_get_record_as_scene_end())
                reset_cache()
            elif ActDataType.SCENE_CAMERA is record.subtype:
                cache['camera'] = record
            elif ActDataType.SCENE_STAGE is record.subtype:
                cache['stage'] = record
            elif ActDataType.SCENE_YEAR is record.subtype:
                cache['year'] = record
            elif ActDataType.SCENE_DATE is record.subtype:
                cache['date'] = record
            elif ActDataType.SCENE_TIME is record.subtype:
                cache['time'] = record
            elif ActDataType.COMMENT is record.subtype:
                tmp.append(_record_as_comment_from(record))
            elif ActDataType.BR is record.subtype:
                continue
            elif ActDataType.PARAGRAPH_START is record.subtype:
                continue
            elif ActDataType.PARAGRAPH_END is record.subtype:
                continue
            elif ActDataType.TEXT is record.subtype:
                tmp.append(_record_as_text_from(record))
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


def _conv_item_data_record(data: dict) -> StructRecord:
    assert isinstance(data, dict)

    persons = data['person']
    items = data['item']
    return StructRecord(
            StructType.ITEM_DATA,
            ActType.NONE,
            '',
            '',
            {'person': persons,
                'item': items,
                })


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


def _format_transition_record(camera: str, stage: str, year: str, date: str,
        time: str) -> str:
    assert isinstance(camera, str)
    assert isinstance(stage, str)
    assert isinstance(year, str)
    assert isinstance(date, str)
    assert isinstance(time, str)

    _camera = just_string_of(camera, 16)
    _stage = just_string_of(stage, 16)
    _year = just_string_of(year, 8)
    _date = just_string_of(date, 8)
    _time = just_string_of(time, 8)

    return f"| {_stage} | {_time} | {_date} | {_year} | {_camera} |"


def _format_transition_record_as_compare(camera: str, stage: str, year: str,
        date: str, time: str, cache: dict) -> str:
    assert isinstance(camera, str)
    assert isinstance(stage, str)
    assert isinstance(year, str)
    assert isinstance(date, str)
    assert isinstance(time, str)
    assert isinstance(cache, dict)

    def _diff(a: str, b: str) -> str:
        if a != b:
            return '↓'
        else:
            return '…'

    _camera = _diff(camera, cache['camera'])
    _stage = _diff(stage, cache['stage'])
    _year = _diff(year, cache['year'])
    _date = _diff(date, cache['date'])
    _time = _diff(time, cache['time'])

    return _format_transition_record(_camera, _stage, _year, _date, _time)


def _get_record_as_scene_end() -> StructRecord:
    return StructRecord(StructType.SCENE_END, ActType.NONE, '', '', '')


def _record_as_comment_from(record: ActionRecord):
    assert isinstance(record, ActionRecord)

    return StructRecord(
            StructType.COMMENT,
            ActType.DATA,
            record.subject,
            record.outline,
            record.note)


def _record_as_action_from(record: ActionRecord):
    assert isinstance(record, ActionRecord)

    return StructRecord(
            StructType.ACTION,
            record.type,
            record.subject,
            record.outline,
            record.note)


def _record_as_scene_data_from(camera: ActionRecord, stage: ActionRecord,
        year: ActionRecord, date: ActionRecord, time: ActionRecord) -> StructRecord:

    return StructRecord(
            StructType.SCENE_DATA,
            ActType.DATA,
            camera.subject,
            stage.subject,
            {'year': year.subject,
                'date': date.subject,
                'time': time.subject,
                })


def _record_as_text_from(record: ActionRecord) -> StructRecord:
    assert isinstance(record, ActionRecord)

    return StructRecord(
            StructType.TEXT,
            ActType.DO,
            record.subject,
            record.outline,
            record.note)


def _record_as_title_from(record: ActionRecord) -> StructRecord:
    assert isinstance(record, ActionRecord)

    return StructRecord(
            _title_type_of(record),
            ActType.DATA,
            record.subject,
            record.outline,
            record.note)


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

    year = str(record.note['year'])
    date = str(record.note['date'])
    time = str(record.note['time'])

    return StructRecord(
            record.type,
            record.act,
            translate_tags_str(record.subject, tags, True, None),
            translate_tags_str(record.outline, tags, True, None),
            {
                'year': translate_tags_str(year, tags, True, None),
                'date': translate_tags_str(date, tags, True, None),
                'time': translate_tags_str(time, tags, True, None),
            })
