"""Format module for struct data."""

# Official Libraries
from dataclasses import dataclass


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
from stobu.types.info import SceneInfo
from stobu.types.struct import StructRecord, StructsData, StructType
from stobu.types.struct import SceneDataInfo, DataInfoType
from stobu.utils import assertion
from stobu.utils.log import logger
from stobu.utils.strings import just_string_of


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


@dataclass
class HeadIndex(object):
    chapter: int
    episode: int
    scene: int


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

    index = HeadIndex(0, 0, 0)


    for record in structs_data.get_data():
        assert isinstance(record, StructRecord)
        if record.type in TITLES:
            if StructType.TITLE_BOOK is record.type:
                ret = _record_as_title_from(record, index)
                if ret:
                    tmp.append(get_format_record_as_br())
                    tmp.append(get_breakline())
                    tmp.append(ret)
                    tmp.append(get_format_record_as_br(2))
            elif StructType.TITLE_CHAPTER is record.type:
                index.chapter += 1
                ret = _record_as_title_from(record, index)
                if ret:
                    tmp.append(get_format_record_as_br())
                    tmp.append(ret)
                    tmp.append(get_format_record_as_br(2))
            elif StructType.TITLE_EPISODE is record.type:
                index.episode += 1
                ret = _record_as_title_from(record, index)
                if ret:
                    tmp.append(get_format_record_as_br())
                    tmp.append(ret)
                    tmp.append(get_format_record_as_br(2))
            elif StructType.TITLE_SCENE is record.type:
                index.scene += 1
                ret = _record_as_title_from(record, index)
                if ret:
                    tmp.append(get_format_record_as_br())
                    tmp.append(ret)
                    tmp.append(get_format_record_as_br(2))
            else:
                tmp.append(_record_as_title_from(record))
        elif StructType.SCENE_DATA is record.type:
            tmp.append(_record_as_scene_data_from(record))
            tmp.append(get_format_record_as_br(2))
        elif StructType.PERSON_DATA is record.type:
            tmp.append(_record_as_person_info_from(record))
            tmp.append(get_format_record_as_br())
        elif StructType.ITEM_DATA is record.type:
            tmp.append(_record_as_item_info_from(record))
            tmp.append(get_format_record_as_br())
        elif StructType.EVENT_DATA is record.type:
            tmp.append(_record_as_event_info_from(record))
            tmp.append(get_format_record_as_br(2))
        elif StructType.COMMENT is record.type:
            if is_comment:
                tmp.append(get_format_record_as_comment(record.subject))
                tmp.append(get_format_record_as_br())
            else:
                continue
        elif StructType.ACTION is record.type:
            tmp.append(_record_as_action_from(record))
            tmp.append(get_format_record_as_br())
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
    indent = get_format_record_as_indent(4)
    indent1 = get_format_record_as_indent(2)

    # persons
    if ActType.BE is act:
        text = f"[{subject}]が{outline}" if outline else f"[{subject}]がいる"
        return f"{indent}{text}"
    elif ActType.COME is act:
        text = f"[{subject}]が{outline}" if outline else f"[{subject}]が来る"
        head = just_string_of('IN', 8)
        return f"{head}{text}"
    elif ActType.GO is act:
        text = f"[{subject}]が{outline}" if outline else f"[{subject}]が出ていく"
        head = just_string_of('OUT', 8)
        return f"{head}{text}"
    # skin
    elif ActType.WEAR is act:
        text = f"{subject}は[{outline}]を着ている"
        return f"{indent}{text}"
    # stage
    elif ActType.PUT is act:
        text = f"<（{subject}）{outline}>" if subject else f"<{outline}>"
        return f"{indent}{text}"
    elif ActType.RID is act:
        text = f"<〜（{subject}）{outline}>" if subject else f"<〜{outline}>"
        return f"{indent}{text}"
    # view
    elif ActType.DRAW is act:
        text = f"（{subject}について）{outline}" if subject else f"{outline}"
        return f"{indent}{text}"
    # info
    elif ActType.EXPLAIN is act:
        text = f"{subject}は{outline}について説明する" if subject else f"{outline}についての説明"
        return f"{indent1}※{text}"
    elif ActType.KNOW is act:
        text = f"{subject}は【{outline}】を知る" if outline else f"【{subject}】を知る"
        return f"{indent1}※{text}"
    elif ActType.KNOWN is act:
        text = f"{subject}は【{outline}】を知っていた" if outline else f"【{subject}】を知っていた"
        return f"{indent1}※{text}"
    elif ActType.REMEMBER is act:
        text = f"{subject}が{outline}を思い出す" if outline else f"{subject}を思い出す"
        return f"{indent1}※{text}"
    # items
    elif ActType.HAVE is act:
        text = f"{subject}は[{outline}]を持っている"
        return f"{indent}{text}"
    elif ActType.DISCARD is act:
        text = f"{subject}が[{outline}]を捨てる"
        return f"{indent}〜{text}"
    # event
    elif ActType.OCCUR is act:
        text = f"【（{subject}）{outline}】" if subject else f"【{outline}】"
        return f"{indent}{text}"
    # dialogue
    elif ActType.TALK is act:
        return f"{subject}「{outline}」"
    elif ActType.THINK is act:
        text = f"（{subject}は{outline}を考える）" if outline else f"（{subject}は考え込む）"
        return f"{indent}{text}"
    elif ActType.VOICE is act:
        return f"{subject}『{outline}』"
    # general
    elif ActType.DO is act:
        text = f"{subject}が{outline}" if outline else f"{subject}が行動する"
        return f"{indent}{text}"
    else:
        return ""


def _record_as_event_info_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    info = assertion.is_instance(record.note, SceneDataInfo)
    data = "、".join(info.data)

    return f"[Ｅ:{data}]"


def _record_as_item_info_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    info = assertion.is_instance(record.note, SceneDataInfo)
    data = "、".join(info.data)

    return f"[Ｉ: {data}]"


def _record_as_person_info_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    info = assertion.is_instance(record.note, SceneDataInfo)
    data = "、".join(info.data)

    return f"[Ｐ: {data}]"


def _record_as_scene_data_from(record: StructRecord) -> str:
    assert isinstance(record, StructRecord)

    info = assertion.is_instance(record.note, SceneInfo)

    camera = info.camera
    stage = info.stage
    year = info.year
    date = info.date
    time = info.time

    return f"○{stage}（{time}）- {date}/{year} 【{camera}】"


def _record_as_title_from(record: StructRecord, index: HeadIndex) -> str:
    assert isinstance(record, StructRecord)
    assert isinstance(index, HeadIndex)

    if StructType.TITLE_BOOK is record.type:
        return f"# {record.subject}"
    elif StructType.TITLE_CHAPTER is record.type:
        return f"## {record.subject}"
    elif StructType.TITLE_EPISODE is record.type:
        return f"### {record.subject}"
    elif StructType.TITLE_SCENE is record.type:
        return f"#### {index.chapter}.{index.episode}.{index.scene} {record.subject}"
    elif StructType.TITLE_TEXT is record.type:
        return f"[{record.subject}]"
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"struct type title in {PROC}"))
        return ""
