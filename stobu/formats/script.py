"""Format module for script data."""

# Official Libraries


# My Modules
from stobu.formats.common import conv_charcounts_from
from stobu.formats.common import get_breakline
from stobu.formats.common import get_format_record_as_br
from stobu.formats.common import head_string_from_elm
from stobu.syss import messages as msg
from stobu.types.count import CountRecord, CountsData
from stobu.types.element import ElmType
from stobu.types.script import ScriptRecord, ScriptsData, ScriptType
from stobu.utils.log import logger


__all__ = (
        'format_scripts_charcounts_data',
        'format_scripts_data',
        )


# Define Constants
PROC = 'FORMAT SCRIPT'


TITLES = [
        ScriptType.TITLE_BOOK,
        ScriptType.TITLE_CHAPTER,
        ScriptType.TITLE_EPISODE,
        ScriptType.TITLE_SCENE,
        ScriptType.TITLE_TEXT,
        ]



NORMAL_SCRIPTS = [
        ScriptType.COMMENT,
        ScriptType.DESCRIPTION,
        ScriptType.DIALOGUE,
        ScriptType.MONOLOGUE,
        ScriptType.SE,
        ]


TALK_SCRIPTS = [
        ScriptType.DIALOGUE,
        ScriptType.MONOLOGUE,
        ]


# Main
def format_scripts_charcounts_data(counts_data: CountsData) -> list:
    assert isinstance(counts_data, CountsData)

    _PROC = f"{PROC}: format data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    current = ElmType.NONE

    tmp.append(get_breakline())
    tmp.append("# SCRIPT char counts:\n")

    for record in counts_data.get_data():
        assert isinstance(record, CountRecord)
        if not current is record.type:
            tmp.append(get_format_record_as_br())
            tmp.append(head_string_from_elm(record.type, 'count'))
            current = record.type
        tmp.append(conv_charcounts_from(record))
        tmp.append(get_format_record_as_br())

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


def format_scripts_data(scripts_data: ScriptsData) -> list:
    assert isinstance(scripts_data, ScriptsData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    is_br_mode = True
    has_first_indent = False

    def reset_br():
        is_br_mode = True
        has_first_indent = False

    for record in scripts_data.get_data():
        assert isinstance(record, ScriptRecord)
        if record.type in TITLES:
            tmp.append(_record_as_title_from(record))
            tmp.append(_get_record_as_br(2))
            reset_br()
        elif ScriptType.PARAGRAPH_START is record.type:
            is_br_mode = False
        elif ScriptType.BR is record.type:
            tmp.append(_get_record_as_br())
            reset_br()
        elif ScriptType.PARAGRAPH_END is record.type:
            tmp.append(_get_record_as_br())
            reset_br()
        elif ScriptType.SPIN is record.type:
            tmp.append(_record_as_spin_from(record))
            tmp.append(_get_record_as_br())
            reset_br()
        elif record.type in NORMAL_SCRIPTS:
            # br and indent
            if is_br_mode:
                if record.type in TALK_SCRIPTS:
                    has_first_indent = True
                else:
                    tmp.append(_get_record_as_indent())
            elif not has_first_indent:
                tmp.append(_get_record_as_indent())
                has_first_indent = True
            # descriptions
            if ScriptType.COMMENT is record.type:
                tmp.append(_record_as_comment_from(record))
            elif ScriptType.DESCRIPTION is record.type:
                tmp.append(_record_as_description_from(record))
            elif ScriptType.DIALOGUE is record.type:
                tmp.append(_record_as_dialogue_from(record))
            elif ScriptType.MONOLOGUE is record.type:
                tmp.append(_record_as_monologue_from(record))
            elif ScriptType.SE is record.type:
                tmp.append(_record_as_se_from(record))
            else:
                pass
            if is_br_mode:
                tmp.append(_get_record_as_br())
        elif ScriptType.NONE is record.type:
            continue
        else:
            logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"script type in {PROC}"))
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


def _get_record_as_br(num: int = 1) -> str:
    assert isinstance(num, int)

    return "\n" * num


def _get_record_as_indent() -> str:
    # NOTE: indent量は設定から決める。とりあえず空白３で
    return "　　　"


def _record_as_comment_from(record: ScriptRecord) -> str:
    return f"<!--{record.subject}-->"


def _record_as_description_from(record: ScriptRecord) -> str:
    assert isinstance(record, ScriptRecord)

    last = '' if record.desc.endswith('。') else '。'

    return f"{record.desc}{last}"


def _record_as_dialogue_from(record: ScriptRecord) -> str:
    assert isinstance(record, ScriptRecord)

    return f"{record.subject}「{record.desc}」"


def _record_as_monologue_from(record: ScriptRecord) -> str:
    assert isinstance(record, ScriptRecord)

    return f"{record.subject}Ｍ『{record.desc}』"


def _record_as_se_from(record: ScriptRecord) -> str:
    assert isinstance(record, ScriptRecord)

    return f"ＳＥ　{record.desc}"


def _record_as_spin_from(record: ScriptRecord) -> str:
    assert isinstance(record, ScriptRecord)

    # NOTE: 場所・時間帯以外の表示をどうするか

    return f"○{record.desc}（{record.note}）"


def _record_as_title_from(record: ScriptRecord) -> str:
    assert isinstance(record, ScriptRecord)

    if ScriptType.TITLE_BOOK is record.type:
        return f"# {record.subject}"
    elif ScriptType.TITLE_CHAPTER is record.type:
        return f"## {record.subject}"
    elif ScriptType.TITLE_EPISODE is record.type:
        return f"### {record.subject}"
    elif ScriptType.TITLE_SCENE is record.type:
        return f"** {record.subject} **"
    elif ScriptType.TITLE_TEXT is record.type:
        return f"[{record.subject}]"
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"script type title in {PROC}"))
        return ""
