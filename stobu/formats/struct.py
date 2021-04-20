"""Format module for struct data."""

# Official Libraries


# My Modules
from stobu.formats.common import conv_charcounts_from
from stobu.formats.common import get_breakline
from stobu.formats.common import get_format_record_as_br
from stobu.formats.common import get_format_record_as_comment
from stobu.formats.common import get_format_record_as_indent
from stobu.formats.common import head_string_from_elm
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.count import CountRecord, CountsData
from stobu.types.element import ElmType
from stobu.types.struct import StructRecord, StructsData, StructType
from stobu.utils.log import logger


__all__ = (
        'format_structs_charcounts_data',
        'format_structs_data',
        )


# Define Constants
PROC = 'FORMAT STRUCT'


TITLES = [
        StructType.TITLE_BOOK,
        StructType.TITLE_CHAPTER,
        StructType.TITLE_EPISODE,
        StructType.TITLE_SCENE,
        StructType.TITLE_TEXT,
        ]


# Main
def format_structs_charcounts_data(counts_data: CountsData) -> list:
    assert isinstance(counts_data, CountsData)

    _PROC = f"{PROC}: format data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    current = ElmType.NONE

    tmp.append(get_breakline())
    tmp.append("# STRUCT char counts:\n")

    for record in counts_data.get_data():
        assert isinstance(record, CountRecord)
        if current is not record.type:
            tmp.append(get_format_record_as_br())
            tmp.append(head_string_from_elm(record.type, 'count'))
            current = record.type
        tmp.append(conv_charcounts_from(record))
        tmp.append(get_format_record_as_br())

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


def format_structs_data(structs_data: StructsData, is_comment: bool) -> list:
    assert isinstance(structs_data, StructsData)
    assert isinstance(is_comment, bool)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    for record in structs_data.get_data():
        assert isinstance(record, StructRecord)
        if record.type in TITLES:
            tmp.append(get_format_record_as_br())
            tmp.append(get_breakline())
            tmp.append(_record_as_title_from(record))
            tmp.append(get_format_record_as_br(2))
        elif StructType.SCENE_DATA is record.type:
            tmp.append(_record_as_scene_data_from(record))
            tmp.append(get_format_record_as_br())
        elif StructType.ITEM_DATA is record.type:
            tmp.append(get_format_record_as_br())
            tmp.append(_record_as_item_data_from(record))
            tmp.append(get_format_record_as_br())
        elif StructType.COMMENT is record.type:
            if is_comment:
                tmp.append(get_format_record_as_comment(record.subject))
                tmp.append(get_format_record_as_br())
            else:
                continue
        elif StructType.ACTION is record.type:
            tmp.append(_record_as_action_from(record))
            tmp.append(get_format_record_as_br())
        elif StructType.FLAG_FORESHADOW is record.type:
            continue
        elif StructType.FLAG_PAYOFF is record.type:
            continue
        elif StructType.NONE is record.type:
            continue
        elif StructType.SCENE_END is record.type:
            continue
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"struct type in {PROC}"), record.type)
            continue

    eliminated = _eliminated_empty_record(tmp)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return eliminated


# Private Functions
def _eliminated_empty_record(base_data: list) -> list:
    assert isinstance(base_data, list)

    tmp = []

    for record in base_data:
        if record:
            tmp.append(record)

    return tmp


def _record_as_action_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    act = record.act
    subject = record.subject
    outline = record.outline

    if ActType.BE is act:
        return f"[{subject}]（{outline}）"
    elif ActType.COME is act:
        return f"in [{subject}]（{outline}）"
    elif ActType.DISCARD is act:
        return f"out [{outline}]（{subject}）"
    elif ActType.DO is act:
        return f"{get_format_record_as_indent(2)}（{subject}）{outline}"
    elif ActType.DRAW is act:
        return f"{get_format_record_as_indent(2)}__{outline}__"
    elif ActType.EXPLAIN is act:
        return f"...（{subject}）{outline}"
    elif ActType.GO is act:
        return f"out [{subject}]（{outline}）"
    elif ActType.HAVE is act:
        return f"in [{outline}]（{subject}）"
    elif ActType.OCCUR is act:
        return f"{get_format_record_as_indent(2)}<_{outline}_>"
    elif ActType.TALK is act:
        return f"{subject}「{outline}」"
    elif ActType.THINK is act:
        return f"{subject}（{outline}）"
    elif ActType.VOICE is act:
        return f"{subject}『{outline}』"
    else:
        return ""


def _record_as_item_data_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    persons = ", ".join(sorted(list(set(record.note['person']))))
    items = ''
    flags = ''
    deflags = ''

    for flag in record.note['flag']:
        subject, outline = flag.split(':')
        flags += f"（{subject}）{outline}／"
    for deflag in record.note['deflag']:
        subject, outline = deflag.split(':')
        deflags += f"（{subject}）{outline}／"

    return f"| _PERSONS_ | {persons} |\n" \
            + f"| _ITEMS_   | {items} |\n" \
            + f"| _FLAGS_   | {flags} |\n" \
            + f"| _DEFLAGS_ | {deflags} |"


def _record_as_scene_data_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    camera = record.subject
    stage = record.outline
    year = record.note['year']
    date = record.note['date']
    time = record.note['time']

    return f"○{stage}（{time}）- {date}/{year} ＜{camera}＞"


def _record_as_title_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    if StructType.TITLE_BOOK is record.type:
        return f"# {record.subject}"
    elif StructType.TITLE_CHAPTER is record.type:
        return f"## {record.subject}"
    elif StructType.TITLE_EPISODE is record.type:
        return f"### {record.subject}"
    elif StructType.TITLE_SCENE is record.type:
        return f"** {record.subject} **"
    elif StructType.TITLE_TEXT is record.type:
        return f"[{record.subject}]"
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"struct type title in {PROC}"))
        return ""
