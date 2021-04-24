"""Common format module."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.types.count import CountRecord
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.log import logger
from stobu.utils.strings import just_string_of


__all__ = (
        'conv_charcounts_from',
        'eliminated_empty_format_records_from',
        'get_breakline',
        'get_breakline_list',
        'get_format_record_as_br',
        'get_format_record_as_comment',
        'get_format_record_as_description',
        'get_format_record_as_dialogue',
        'get_format_record_as_indent',
        'get_format_record_as_monologue',
        'head_string_from_elm',
        )


# Define Constants
PROC = 'FORMAT COMMON'


TITLES = {
        ElmType.BOOK: 'BOOK',
        ElmType.CHAPTER: 'CHAPTER',
        ElmType.EPISODE: 'EPISODE',
        ElmType.SCENE: 'SCENE',
        ElmType.NONE: '',
        }


# Main
def conv_charcounts_from(record: CountRecord) -> str:
    assert isinstance(record, CountRecord)

    title = record.title
    total = record.total
    space = record.space
    real = total - space
    lines = round(record.lines, 3)
    papers = round(record.papers, 3)

    return f"- {just_string_of(title, 16)}: {papers}p/{lines}n [{total}c ({real}/{space})c]"


def eliminated_empty_format_records_from(origin_data: list) -> list:
    assert isinstance(origin_data, list)

    tmp = []

    for record in origin_data:
        if record and isinstance(record, str):
            tmp.append(record)

    return tmp


def get_breakline(num: int = 8) -> str:
    assert isinstance(num, int)

    return "--------" * num + '\n'


def get_breakline_list() -> list:
    return [get_breakline()]


def get_format_record_as_br(num: int = 1) -> str:
    assert isinstance(num, int)

    return "\n" * num


def get_format_record_as_comment(comment: str) -> str:
    assert isinstance(comment, str)

    return f"<!--{comment}-->"


def get_format_record_as_description(desc: str) -> str:
    assert isinstance(desc, str)

    suffix = '' if desc.endswith('。') else '。'

    return f"{desc}{suffix}"


def get_format_record_as_dialogue(desc: str, subject: str = None) -> str:
    assert isinstance(desc, str)

    prefix = assertion.is_str(subject) if subject else ''

    return f"{prefix}「{desc}」"


def get_format_record_as_indent(num: int = 1) -> str:
    assert isinstance(num, int)

    return '　' * num


def get_format_record_as_monologue(desc: str, subject: str = None) -> str:
    assert isinstance(desc, str)

    prefix = assertion.is_str(subject) if subject else ''

    return f"{prefix}『{desc}』"


def head_string_from_elm(elm: ElmType, title: str) -> str:
    assert isinstance(elm, ElmType)
    assert isinstance(title, str)

    head = TITLES[elm]

    return f"### {head}: {title}\n\n"
