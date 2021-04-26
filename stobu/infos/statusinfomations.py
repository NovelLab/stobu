"""Status info creator module."""

# Official Libraries


# My Modules
from stobu.core.nametagcreator import get_calling_tags
from stobu.elms.stages import StageItem
from stobu.infos.common import get_record_as_data_title, get_record_as_splitter
from stobu.syss import messages as msg
from stobu.tools.datareader import stage_item_of
from stobu.tools.pathgetter import filepaths_by_elm
from stobu.types.action import ActType
from stobu.types.element import ElmType
from stobu.types.info import InfosData, InfoRecord, InfoType
from stobu.types.info import PersonStateInfo, PersonStateType
from stobu.types.info import StageStateInfo, StageStateType
from stobu.types.info import SceneInfo
from stobu.utils import assertion
from stobu.utils.filepath import basename_of
from stobu.utils.log import logger


__all__ = (
        'person_status_info_from',
        'stage_status_info_from',
        )


# Define Constants
PROC = 'INFO STATUS'


# Main
def person_status_info_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    _PROC = f"{PROC}: person status"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    base_data = _base_person_status_data_from(infos_data)

    reordered = _reorder_each_persons(base_data)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return InfosData(reordered)


def stage_status_info_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    _PROC = f"{PROC}: stage status"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    base_data = _base_stage_status_data_from(infos_data)

    reordered = _reorder_each_stages(base_data)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return InfosData(reordered)


# Sub processes
def _base_person_status_data_from(infos_data: InfosData) -> list:
    assert isinstance(infos_data, InfosData)

    _PROC = f"{PROC}: base person data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    index = 0

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_person_info_from(index, record)
            if ret:
                tmp.append(ret)
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


def _base_stage_status_data_from(infos_data: InfosData) -> list:
    assert isinstance(infos_data, InfosData)

    _PROC = f"{PROC}: base stage data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []
    index = 0
    stage = 'None'

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_stage_info_from(index, stage, record)
            if ret:
                tmp.append(ret)
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        elif InfoType.SCENE_HEAD is record.type:
            info = assertion.is_instance(record.note, SceneInfo)
            stage = info.stage
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


def _reorder_each_persons(base_data: list) -> list:
    assert isinstance(base_data, list)

    _PROC = f"{PROC}: reorder person data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []

    persons = _get_persons_list()

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title("PERSON STATUS TRANSITIONS"))

    for person in persons:
        tmp.append(_get_record_as_data_splitter(ElmType.PERSON))
        for record in base_data:
            assert isinstance(record, InfoRecord)
            info = assertion.is_instance(record.note, PersonStateInfo)
            if info.subject == person:
                tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


def _reorder_each_stages(base_data: list) -> list:
    assert isinstance(base_data, list)

    _PROC = f"{PROC}: reorder stage data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = []

    stages = _get_stages_list()

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title("STAGE STATUS TRANSITIONS"))

    for stage in stages:
        tmp.append(_get_record_as_data_splitter(ElmType.STAGE))
        for record in base_data:
            assert isinstance(record, InfoRecord)
            info = assertion.is_instance(record.note, StageStateInfo)
            if info.stage == stage:
                tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))

    return tmp


# Private Functions
def _get_persons_list() -> list:
    callings = get_calling_tags()

    tmp = []

    for key, data in callings.items():
        tmp.append(data['S'])

    return sorted(tmp)


def _get_record_as_data_splitter(elm: ElmType) -> InfoRecord:
    assert isinstance(elm, ElmType)

    if ElmType.PERSON is elm:
        return InfoRecord(InfoType.PERSON_STATE_INFO, ActType.DATA, '', '',
                PersonStateInfo(PersonStateType.NONE, 0, '', '', ''))
    else:
        return InfoRecord(InfoType.STAGE_STATE_INFO, ActType.DATA, '', '',
                StageStateInfo(StageStateType.NONE, 0, '', '', ''))


def _get_stages_list() -> list:
    tmp = []

    paths = filepaths_by_elm(ElmType.STAGE)

    for fname in paths:
        assert isinstance(fname, str)
        tmp.append(stage_item_of(fname, StageItem.NAME))

    return sorted(tmp)


def _record_as_person_info_from(index: int, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(record, InfoRecord)

    info_type = PersonStateType.NONE

    if ActType.WEAR is record.act:
        info_type = PersonStateType.SKIN
    elif ActType.KNOW is record.act:
        info_type = PersonStateType.INFO
    elif ActType.KNOWN is record.act:
        info_type = PersonStateType.INFO
    elif ActType.FEEL is record.act:
        info_type = PersonStateType.STATE
    else:
        return None

    info = PersonStateInfo(info_type, index, record.subject, record.outline, record.note)

    return InfoRecord(InfoType.PERSON_STATE_INFO, ActType.DATA,
            record.subject, record.outline, info)

def _record_as_stage_info_from(index: int, stage: str, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(stage, str)
    assert isinstance(record, InfoRecord)

    info_type = StageStateType.NONE

    subject = record.subject

    if ActType.DRAW is record.act:
        info_type = StageStateType.VIEW
        if not record.subject:
            subject = record.outline
    elif ActType.PUT is record.act:
        info_type = StageStateType.ITEM
    elif ActType.RID is record.act:
        info_type = StageStateType.ITEM
    else:
        return None

    return InfoRecord(InfoType.STAGE_STATE_INFO, ActType.DATA, '', '',
            StageStateInfo(info_type, index, stage, subject, record.note))
