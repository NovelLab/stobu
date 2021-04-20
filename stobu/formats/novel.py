"""Format module for novel data."""

# Official Libraries


# My Modules
from stobu.formats.common import conv_charcounts_from
from stobu.formats.common import get_breakline
from stobu.formats.common import get_format_record_as_br, get_format_record_as_comment
from stobu.formats.common import get_format_record_as_indent
from stobu.formats.common import get_format_record_as_description, get_format_record_as_dialogue
from stobu.formats.common import head_string_from_elm
from stobu.syss import messages as msg
from stobu.types.count import CountRecord, CountsData
from stobu.types.element import ElmType
from stobu.types.novel import NovelRecord, NovelsData, NovelType
from stobu.utils.log import logger


__all__ = (
        'format_novels_charcounts_data',
        'format_novels_data',
        )


# Define Constants
PROC = 'FORMAT NOVEL'


TITLES = [
        NovelType.TITLE_BOOK,
        NovelType.TITLE_CHAPTER,
        NovelType.TITLE_EPISODE,
        NovelType.TITLE_SCENE,
        NovelType.TITLE_TEXT,
        ]


NORAL_DESCS = [
        NovelType.COMMENT,
        NovelType.DESCRIPTION,
        NovelType.DIALOGUE,
        NovelType.PLAIN,
        ]


# Main
def format_novels_charcounts_data(counts_data: CountsData) -> list:
    assert isinstance(counts_data, CountsData)

    _PROC = f"{PROC}: format data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    current = ElmType.NONE

    tmp.append(get_breakline())
    tmp.append("# NOVEL char counts:\n")

    for record in counts_data.get_data():
        assert isinstance(record, CountRecord)
        if current is not record.type:
            tmp.append(get_format_record_as_br())
            tmp.append(head_string_from_elm(record.type, 'count'))
            current = record.type
        tmp.append(conv_charcounts_from(record))
        tmp.append(get_format_record_as_br())

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


def format_novels_data(novels_data: NovelsData, is_comment: bool) -> list:
    assert isinstance(novels_data, NovelsData)
    assert isinstance(is_comment, bool)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    is_br_mode = True
    has_first_indent = False

    def reset_br():
        is_br_mode = True
        has_first_indent = False

    for record in novels_data.get_data():
        assert isinstance(record, NovelRecord)
        if record.type in TITLES:
            tmp.append(_record_as_title_from(record))
            tmp.append(get_format_record_as_br(2))
        elif NovelType.PARAGRAPH_START is record.type:
            is_br_mode = False
        elif NovelType.PARAGRAPH_END is record.type:
            tmp.append(get_format_record_as_br())
            reset_br()
        elif NovelType.BR is record.type:
            tmp.append(get_format_record_as_br())
            reset_br()
        elif record.type in NORAL_DESCS:
            # br and indent
            if is_br_mode:
                if NovelType.DIALOGUE is record.type:
                    has_first_indent = True
                else:
                    tmp.append(get_format_record_as_indent())
            elif not has_first_indent:
                tmp.append(get_format_record_as_indent())
                has_first_indent = True
            # descriptions
            if NovelType.COMMENT is record.type:
                if is_comment:
                    tmp.append(get_format_record_as_comment(record.subject))
                else:
                    continue
            elif NovelType.DESCRIPTION is record.type:
                tmp.append(get_format_record_as_description(record.desc))
            elif NovelType.DIALOGUE is record.type:
                tmp.append(get_format_record_as_dialogue(record.desc))
            elif NovelType.PLAIN is record.type:
                tmp.append(record.desc)
            else:
                pass
            if is_br_mode:
                tmp.append(get_format_record_as_br())
        elif NovelType.NONE is record.type:
            continue
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"novel type in {PROC}"))
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


def _record_as_title_from(record: NovelRecord) -> str:
    assert isinstance(record, NovelRecord)

    if NovelType.TITLE_BOOK is record.type:
        return f"# {record.subject}"
    elif NovelType.TITLE_CHAPTER is record.type:
        return f"## {record.subject}"
    elif NovelType.TITLE_EPISODE is record.type:
        return f"### {record.subject}"
    elif NovelType.TITLE_SCENE is record.type:
        return f"** {record.subject} **"
    elif NovelType.TITLE_TEXT is record.type:
        return f"[{record.subject}]"
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"novel type title in {PROC}"))
        return ""
