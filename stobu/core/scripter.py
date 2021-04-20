"""Build Script module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.formats.script import format_scripts_data
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_text_list, translate_tags_str
from stobu.types.action import ActDataType, ActionRecord, ActionsData, ActType
from stobu.types.action import NORMAL_ACTIONS
from stobu.types.output import OutputsData
from stobu.types.script import ScriptRecord, ScriptsData, ScriptType
from stobu.utils.dicts import dict_sorted
from stobu.utils.log import logger


__all__ = (
        'outputs_data_from_scripts_data',
        'scripts_data_from',
        )


# Define Constants
PROC = 'BUILD SCRIPT'


ACT_TITLES = [
        ActDataType.BOOK_TITLE,
        ActDataType.CHAPTER_TITLE,
        ActDataType.EPISODE_TITLE,
        ActDataType.SCENE_TITLE,
        ActDataType.SCENE_HEAD,
        ]


ACT_TALKS = [
        ActType.EXPLAIN,
        ActType.TALK,
        ActType.THINK,
        ]


ACTIONS = [
        ScriptType.COMMENT,
        ScriptType.DESCRIPTION,
        ScriptType.DIALOGUE,
        ScriptType.MONOLOGUE,
        ]


# Main
def scripts_data_from(actions_data: ActionsData, tags: dict) -> ScriptsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    base_data = _base_scripts_data_from(actions_data)

    updated = update_data_tags(base_data, tags)

    eliminated = _eliminate_empty_records(updated)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return ScriptsData(eliminated)


def outputs_data_from_scripts_data(scripts_data: ScriptsData, tags: dict,
        is_comment: bool = False) -> OutputsData:
    assert isinstance(scripts_data, ScriptsData)
    assert isinstance(tags, dict)

    _PROC = f"{PROC}: convert outputs data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    formatted = format_scripts_data(scripts_data, is_comment)

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


def update_data_tags(origin_data: list, tags: dict) -> list:
    assert isinstance(origin_data, list)
    assert isinstance(tags, dict)

    tmp = []
    callings = get_calling_tags()

    for record in origin_data:
        assert isinstance(record, ScriptRecord)
        if record.type in ACTIONS:
            tmp.append(_update_tags_desc_record(record, tags, callings))
        elif ScriptType.SPIN is record.type:
            tmp.append(_update_tags_spin_record(record, tags))
        else:
            tmp.append(record)

    return tmp


# Private Functions
def _base_scripts_data_from(actions_data: ActionsData) -> list:
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
                tmp.append(
                        _record_as_spin_from(
                            cache['camera'], cache['stage'], cache['time']))
            elif ActDataType.SCENE_END is record.subtype:
                reset_cache()
                tmp.append(_get_record_as_br())
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
                tmp.append(_get_record_as_br())
            elif ActDataType.PARAGRAPH_START is record.subtype:
                tmp.append(_get_record_as_paragraph_start())
            elif ActDataType.PARAGRAPH_END is record.subtype:
                tmp.append(_get_record_as_paragraph_end())
            elif ActDataType.TEXT is record.subtype:
                tmp.append(_record_as_description_from(record))
            else:
                logger.warning(msg.ERR_FAIL_UNKNOWN_DATA.format(data=f"act data sub type in {PROC}"))
                continue
        elif record.type in NORMAL_ACTIONS:
            if record.type in ACT_TALKS:
                if ActType.TALK is record.type:
                    tmp.append(_record_as_dialogue_from(record))
                else:
                    tmp.append(_record_as_monologue_from(record))
            else:
                tmp.append(_record_as_description_from(record))
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
        assert isinstance(record, ScriptRecord)
        if record.type in [ScriptType.COMMENT, ScriptType.DESCRIPTION, ScriptType.DIALOGUE, ScriptType.MONOLOGUE, ScriptType.SE]:
            if ScriptType.COMMENT is record.type:
                if record.subject:
                    tmp.append(record)
            elif ScriptType.SE is record.type:
                if record.subject:
                    tmp.append(record)
            else:
                if record.desc:
                    tmp.append(record)
        else:
            tmp.append(record)

    return tmp


def _get_record_as_br() -> ScriptRecord:
    return ScriptRecord(ScriptType.BR, '', '', '')


def _get_record_as_paragraph_end() -> ScriptRecord:
    return ScriptRecord(ScriptType.PARAGRAPH_END, '', '', '')


def _get_record_as_paragraph_start() -> ScriptRecord:
    return ScriptRecord(ScriptType.PARAGRAPH_START, '', '', '')



def _record_as_comment_from(record: ActionRecord) -> ScriptRecord:
    assert isinstance(record, ActionRecord)

    return ScriptRecord(
            ScriptType.COMMENT,
            record.subject,
            record.outline,
            record.note)


def _record_as_description_from(record: ActionRecord) -> ScriptRecord:
    assert isinstance(record, ActionRecord)

    return ScriptRecord(
            ScriptType.DESCRIPTION,
            record.subject,
            record.desc,
            record.note)


def _record_as_dialogue_from(record: ActionRecord) -> ScriptRecord:
    assert isinstance(record, ActionRecord)

    return ScriptRecord(
            ScriptType.DIALOGUE,
            record.subject,
            record.desc,
            record.note)


def _record_as_monologue_from(record: ActionRecord) -> ScriptRecord:
    assert isinstance(record, ActionRecord)

    return ScriptRecord(
            ScriptType.MONOLOGUE,
            record.subject,
            record.desc,
            record.note)


def _record_as_se_from(record: ActionRecord) -> ScriptRecord:
    assert isinstance(record, ActionRecord)

    return ScriptRecord(
            ScriptType.SE,
            record.subject,
            record.outline,
            record.note)


def _record_as_spin_from(camera: ActionRecord, stage: ActionRecord,
        time: ActionRecord) -> ScriptRecord:
    assert isinstance(camera, ActionRecord)
    assert isinstance(stage, ActionRecord)
    assert isinstance(time, ActionRecord)

    subject = camera.subject
    outline = stage.subject
    note = time.subject
    return ScriptRecord(
            ScriptType.SPIN,
            subject,
            outline,
            note)


def _record_as_title_from(record: ActionRecord) -> ScriptRecord:
    assert isinstance(record, ActionRecord)

    return ScriptRecord(
            _title_type_of(record),
            record.subject,
            record.outline,
            record.note)


def _title_type_of(record: ActionRecord) -> ScriptType:
    assert isinstance(record, ActionRecord)

    if ActDataType.BOOK_TITLE is record.subtype:
        return ScriptType.TITLE_BOOK
    elif ActDataType.CHAPTER_TITLE is record.subtype:
        return ScriptType.TITLE_CHAPTER
    elif ActDataType.EPISODE_TITLE is record.subtype:
        return ScriptType.TITLE_EPISODE
    elif ActDataType.SCENE_TITLE:
        return ScriptType.TITLE_SCENE
    elif ActDataType.SCENE_HEAD:
        return ScriptType.TITLE_TEXT
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"title type in {PROC}"))
        return ScriptType.NONE


def _update_tags_desc_record(record: ScriptRecord, tags: dict,
        callings: dict) -> ScriptRecord:
    assert isinstance(record, ScriptRecord)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)

    if record.subject in callings:
        calling = dict_sorted(callings[record.subject], True)
        return ScriptRecord(
            record.type,
            translate_tags_str(record.subject, tags, True, None),
            translate_tags_str(record.desc, calling),
            translate_tags_str(record.note, calling),
            )
    else:
        return ScriptRecord(
                record.type,
                translate_tags_str(record.subject, tags, True, None),
                record.desc,
                record.note)


def _update_tags_spin_record(record: ScriptRecord, tags: dict) -> ScriptRecord:
    assert isinstance(record, ScriptRecord)
    assert isinstance(tags, dict)

    return ScriptRecord(
            record.type,
            translate_tags_str(record.subject, tags, True, None),
            translate_tags_str(record.desc, tags, True, None),
            translate_tags_str(record.note, tags, True, None),
            )
