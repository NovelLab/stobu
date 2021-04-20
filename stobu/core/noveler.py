"""Build Novel module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.formats.novel import format_novels_data
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_text_list, translate_tags_str
from stobu.types.action import ActDataType, ActionRecord, ActionsData, ActType
from stobu.types.action import NORMAL_ACTIONS
from stobu.types.novel import NovelRecord, NovelsData, NovelType
from stobu.types.output import OutputsData
from stobu.utils.dicts import dict_sorted
from stobu.utils.log import logger


__all__ = (
        'novels_data_from',
        'outputs_data_from_novels_data',
        )


# Define Constants
PROC = 'BUILD NOVEL'


ACT_TITLES = [
        ActDataType.BOOK_TITLE,
        ActDataType.CHAPTER_TITLE,
        ActDataType.EPISODE_TITLE,
        ActDataType.SCENE_TITLE,
        ActDataType.SCENE_HEAD,
        ]


SCENE_DATAS = [
        ActDataType.SCENE_CAMERA,
        ActDataType.SCENE_STAGE,
        ActDataType.SCENE_YEAR,
        ActDataType.SCENE_DATE,
        ActDataType.SCENE_TIME,
        ]


ACTIONS = [
        NovelType.COMMENT,
        NovelType.DESCRIPTION,
        NovelType.DIALOGUE,
        NovelType.PLAIN,
        ]


# Main
def novels_data_from(actions_data: ActionsData, tags: dict) -> NovelsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    base_data = _base_novels_data_from(actions_data)

    updated = update_data_tags(base_data, tags)

    eliminated = _eliminate_empty_records(updated)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return NovelsData(eliminated)


def outputs_data_from_novels_data(novels_data: NovelsData, tags: dict) -> OutputsData:
    assert isinstance(novels_data, NovelsData)
    assert isinstance(tags, dict)

    _PROC = f"{PROC}: convert outputs data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    formatted = format_novels_data(novels_data)

    translated = translate_tags_text_list(formatted, tags)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return OutputsData(translated)


def update_data_tags(origin_data: list, tags: dict) -> list:
    assert isinstance(origin_data, list)
    assert isinstance(tags, dict)

    tmp = []
    callings = get_calling_tags()

    for record in origin_data:
        assert isinstance(record, NovelRecord)
        if record.type in ACTIONS:
            tmp.append(_update_tags_desc_record(record, tags, callings))
        else:
            tmp.append(record)

    return tmp


# Private Functions
def _base_novels_data_from(actions_data: ActionsData) -> list:
    assert isinstance(actions_data, ActionsData)

    tmp = []

    for record in actions_data.get_data():
        assert isinstance(record, ActionRecord)
        if ActType.DATA is record.type:
            if record.subtype in ACT_TITLES:
                tmp.append(_record_as_title_from(record))
            elif ActDataType.SCENE_START is record.subtype:
                tmp.append(_get_record_as_br())
            elif ActDataType.SCENE_END is record.subtype:
                tmp.append(_get_record_as_br())
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
            elif record.subtype in SCENE_DATAS:
                # NOTE: 何か利用する場合はここでキャッシュ
                continue
            else:
                logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"act type in {PROC}"))
                continue
        elif record.type in NORMAL_ACTIONS:
            if ActType.TALK is record.type:
                tmp.append(_record_as_dialogue_from(record))
            else:
                tmp.append(_record_as_description_from(record))
        elif record.type in [ActType.NONE, ActType.SAME]:
            continue
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"act type in {PROC}"))
            continue

    return tmp


def _eliminate_empty_records(base_data: list) -> list:
    assert isinstance(base_data, list)

    tmp = []

    for record in base_data:
        assert isinstance(record, NovelRecord)
        if record.type in [NovelType.COMMENT, NovelType.DESCRIPTION, NovelType.DIALOGUE,
                 NovelType.PLAIN]:
            if NovelType.COMMENT is record.type:
                if record.subject:
                    tmp.append(record)
            else:
                if record.desc:
                    tmp.append(record)
        else:
            tmp.append(record)

    return tmp


def _get_record_as_br() -> NovelRecord:
    return NovelRecord(NovelType.BR, '', '', '')


def _get_record_as_paragraph_end() -> NovelRecord:
    return NovelRecord(NovelType.PARAGRAPH_END, '', '', '')


def _get_record_as_paragraph_start() -> NovelRecord:
    return NovelRecord(NovelType.PARAGRAPH_START, '', '', '')


def _record_as_comment_from(record: ActionRecord) -> NovelRecord:
    return NovelRecord(
            NovelType.COMMENT,
            record.subject,
            record.outline,
            record.note)


def _record_as_description_from(record: ActionRecord) -> NovelRecord:
    return NovelRecord(
            NovelType.DESCRIPTION,
            record.subject,
            record.desc,
            record.note)


def _record_as_dialogue_from(record: ActionRecord) -> NovelRecord:
    return NovelRecord(
            NovelType.DIALOGUE,
            record.subject,
            record.desc,
            record.note)


def _record_as_title_from(record: ActionRecord) -> NovelRecord:
    return NovelRecord(
            _title_type_of(record),
            record.subject,
            record.outline,
            record.note)


def _title_type_of(record: ActionRecord) -> NovelType:
    assert isinstance(record, ActionRecord)

    if ActDataType.BOOK_TITLE is record.subtype:
        return NovelType.TITLE_BOOK
    elif ActDataType.CHAPTER_TITLE is record.subtype:
        return NovelType.TITLE_CHAPTER
    elif ActDataType.EPISODE_TITLE is record.subtype:
        return NovelType.TITLE_EPISODE
    elif ActDataType.SCENE_TITLE:
        return NovelType.TITLE_SCENE
    elif ActDataType.SCENE_HEAD:
        return NovelType.TITLE_TEXT
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"title type in {PROC}"))
        return NovelType.NONE


def _update_tags_desc_record(record: NovelRecord, tags: dict, callings: dict) -> NovelRecord:
    assert isinstance(record, NovelRecord)
    assert isinstance(tags, dict)
    assert isinstance(callings, dict)

    if record.subject in callings:
        calling = dict_sorted(callings[record.subject], True)
        return NovelRecord(
                record.type,
                translate_tags_str(record.subject, tags, True, None),
                translate_tags_str(record.desc, calling),
                translate_tags_str(record.note, calling),
                )
    else:
        return NovelRecord(
                record.type,
                translate_tags_str(record.subject, tags, True, None),
                record.desc,
                record.note)
