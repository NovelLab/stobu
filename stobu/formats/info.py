"""Format module for scene info data."""

# Official Libraries


# My Modules
from stobu.formats.common import get_breakline
from stobu.formats.common import get_format_record_as_br
from stobu.formats.common import eliminated_empty_format_records_from
from stobu.syss import messages as msg
from stobu.types.info import InfoRecord, InfosData, InfoType, SceneInfo
from stobu.types.info import INFO_TITLES
from stobu.types.info import FlagInfo, FlagType
from stobu.types.info import PersonInfo, PersonInfoType
from stobu.types.info import FashionInfo
from stobu.types.info import KnowledgeInfo, KnowledgeInfoType
from stobu.utils import assertion
from stobu.utils.log import logger
from stobu.utils.strings import just_string_of


__all__ = (
        'format_infos_data',
        )


# Define Constants
PROC = 'FORMAT INFO'


# Main
def format_infos_data(infos_data: InfosData, is_comment: bool) -> list:
    assert isinstance(infos_data, InfosData)
    assert isinstance(is_comment, bool)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if record.type in INFO_TITLES:
            pass
        elif InfoType.DATA_TITLE is record.type:
            tmp.append(_record_as_data_title_from(record))
            tmp.append(get_format_record_as_br(2))
        elif InfoType.SCENE_HEAD is record.type:
            pass
        elif InfoType.SCENE_TRANSITION is record.type:
            ret = _record_as_transition_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.FLAG_INFO is record.type:
            ret = _record_as_flag_info_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.PERSON_INFO is record.type:
            ret = _record_as_person_info_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.FASHION_INFO is record.type:
            ret = _record_as_fashion_info_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.KNOWLEDGE_INFO is record.type:
            ret = _record_as_knowledge_info_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.COMMENT is record.type:
            if is_comment:
                pass
            else:
                continue
        elif InfoType.ACTION is record.type:
            pass
        elif InfoType.FLAG_FORESHADOW is record.type:
            pass
        elif InfoType.FLAG_PAYOFF is record.type:
            pass
        elif InfoType.SPLITTER is record.type:
            tmp.append(get_breakline())
        elif record.type in [InfoType.NONE, InfoType.SCENE_END]:
            pass
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"info type in {PROC}"))
            continue

    eliminated = eliminated_empty_format_records_from(tmp)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return eliminated


# Private Functions
def _record_as_data_title_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    return f"{record.subject}"


def _record_as_fashion_info_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, FashionInfo)

    head = info.index
    subject = info.subject
    outline = info.outline

    if head < 0:
        head = subject = outline = '----'
    else:
        outline = f"[{outline}]"

    _head = just_string_of(str(head), 4)
    _subject = just_string_of(subject, 16)
    _outline = just_string_of(outline, 32)

    return f"| {_head} | {_subject} | {_outline} |"


def _record_as_flag_info_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, FlagInfo)

    head = ''
    subject_a = ''
    flag = ''
    subject_b = ''
    deflag = ''

    if FlagType.FLAG is info.type:
        head = info.index
        subject_a = info.subject
        flag = info.flag
    elif FlagType.DEFLAG is info.type:
        head = info.index
        subject_b = info.subject
        deflag = info.flag
    else:
        head = subject_a = flag = subject_b = deflag = '----'

    _head = just_string_of(str(head), 4)
    _subject_a = just_string_of(subject_a, 16)
    _flag = just_string_of(flag, 32)
    _subject_b = just_string_of(subject_b, 16)
    _deflag = just_string_of(deflag, 32)

    return f"| {_head} | {_subject_a} | {_flag} | {_subject_b} | {_deflag} |"


def _record_as_knowledge_info_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, KnowledgeInfo)

    head = info.index
    subject = info.subject
    outline = info.outline
    old_know = ''

    if KnowledgeInfoType.EXPLAIN is info.type:
        subject = f"{subject}"
        outline = f"※{outline}"
    elif KnowledgeInfoType.KNOW is info.type:
        subject = f"{subject}"
    elif KnowledgeInfoType.KNOWN is info.type:
        subject = f"{subject}"
        old_know = f"（{outline}）"
        outline = ''
    elif KnowledgeInfoType.REMEMBER is info.type:
        subject = f"{subject}"
        old_know = f"〜{outline}"
        outline = ''
    elif KnowledgeInfoType.NONE is info.type:
        head = subject = outline = old_know = '----'
    else:
        return None

    _head = just_string_of(str(head), 4)
    _subject = just_string_of(subject, 16)
    _outline = just_string_of(outline, 32)
    _old_know = just_string_of(old_know, 32)

    return f"| {_head} | {_subject} | {_outline} | {_old_know} |"


def _record_as_person_info_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, PersonInfo)

    head = info.index
    info_sub = ''
    subject = info.subject
    outline = info.outline

    if PersonInfoType.BE is info.type:
        info_sub = f"［{subject}］"
    elif PersonInfoType.COME is info.type:
        info_sub = f"in {subject}"
    elif PersonInfoType.GO is info.type:
        info_sub = f"out {subject}"
    else:
        head = info_sub = outline = '----'

    _head = just_string_of(str(head), 4)
    _subject = just_string_of(info_sub, 16)
    _outline = just_string_of(outline, 48)

    return f"| {_head} | {_subject} | {_outline} |"


def _record_as_transition_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, SceneInfo)

    camera = just_string_of(info.camera, 16)
    stage = just_string_of(info.stage, 16)
    year = just_string_of(info.year, 8)
    date = just_string_of(info.date, 8)
    time = just_string_of(info.time, 8)

    return f"| {stage} | {time} | {date} | {year} | {camera} |"
