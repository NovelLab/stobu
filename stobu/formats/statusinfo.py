"""Format module for status info data."""

# Official Libraries


# My Modules
from stobu.formats.common import get_breakline, get_format_record_as_br
from stobu.formats.common import eliminated_empty_format_records_from
from stobu.syss import messages as msg
from stobu.types.info import InfosData, InfoRecord, InfoType, SceneInfo
from stobu.types.info import INFO_TITLES
from stobu.types.info import PersonStateInfo, PersonStateType
from stobu.types.info import StageStateInfo, StageStateType
from stobu.utils import assertion
from stobu.utils.log import logger
from stobu.utils.strings import just_string_of


__all__ = (
        'format_status_info_data',
        )


# Define Constants
PROC = 'FORMAT STATUS INFO'


# Main
def format_status_info_data(infos_data: InfosData, is_comment: bool) -> list:
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
        elif InfoType.SPLITTER is record.type:
            tmp.append(get_breakline())
        elif InfoType.PERSON_STATE_INFO is record.type:
            ret = _record_as_person_state_info_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.STAGE_STATE_INFO is record.type:
            ret = _record_as_stage_state_info_from(record)
            if ret:
                tmp.append(ret)
                tmp.append(get_format_record_as_br())
        elif InfoType.COMMENT is record.type:
            if is_comment:
                pass
            else:
                continue
        else:
            continue

    eliminated = eliminated_empty_format_records_from(tmp)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return eliminated


# Private Functions
def _record_as_data_title_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    return f"{record.subject}"


def _record_as_person_state_info_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, PersonStateInfo)

    head = info.index
    subject = info.subject
    outline = info.outline
    skin = state = pinfo = ''

    if PersonStateType.INFO is info.type:
        pinfo = outline
    elif PersonStateType.SKIN is info.type:
        skin = outline
    elif PersonStateType.STATE is info.type:
        state = outline
    elif PersonStateType.NONE is info.type:
        head = skin = state = pinfo = '----'
    else:
        return None

    _head = just_string_of(str(head), 4)
    _subject = just_string_of(subject, 16)
    _skin = just_string_of(skin, 16)
    _state = just_string_of(state, 16)
    _pinfo = just_string_of(pinfo, 32)

    return f"| {_head} | {_subject} | {_skin} | {_state} | {_pinfo} |"


def _record_as_stage_state_info_from(record: InfoRecord) -> str:
    assert isinstance(record, InfoRecord)

    info = assertion.is_instance(record.note, StageStateInfo)

    head = info.index
    stage = info.stage
    item = info.outline
    view = ''

    if StageStateType.ITEM is info.type:
        item = info.outline
        view = ''
    elif StageStateType.VIEW is info.type:
        item = ''
        view = info.outline
    elif StageStateType.NONE is info.type:
        head = stage = item = view = '----'
    else:
        return None

    _head = just_string_of(str(head), 4)
    _stage = just_string_of(stage, 16)
    _item = just_string_of(item, 16)
    _view = just_string_of(view, 32)

    return f"| {_head} | {_stage} | {_item} | {_view} |"
