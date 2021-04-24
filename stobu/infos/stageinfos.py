"""Stage info module."""

# Official Libraries


# My Modules
from stobu.infos.common import get_record_as_data_title, get_record_as_splitter
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import StageInfo, StageInfoType
from stobu.types.info import SceneInfo
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'stage_infos_from',
        )


# Define Constants
PROC = 'INFO STAGE'


# Main
def stage_infos_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    index = 0
    current = None

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title('STAGE INFOS'))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_stage_info_from(index, current, record)
            if ret:
                tmp.append(ret)
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_splitter())
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        elif InfoType.SCENE_HEAD is record.type:
            info = assertion.is_instance(record.note, SceneInfo)
            current = info.stage
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return InfosData(tmp)


# Private Functions
def _get_record_as_splitter() -> InfoRecord:
    return InfoRecord(InfoType.STAGE_INFO, ActType.DATA, '', '',
            StageInfo(StageInfoType.NONE, -1, '', '', '', ''))


def _record_as_stage_info_from(index: int, stage: str, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(stage, str)
    assert isinstance(record, InfoRecord)

    info_type = StageInfoType.NONE

    if ActType.DRAW is record.act:
        info_type = StageInfoType.DRAW
    elif ActType.PUT is record.act:
        info_type = StageInfoType.PUT
    elif ActType.RID is record.act:
        info_type = StageInfoType.RID
    else:
        return None

    info = StageInfo(info_type, index, stage, record.subject, record.outline, record.note)

    return InfoRecord(InfoType.STAGE_INFO, record.act, record.subject,
                record.outline, info)
