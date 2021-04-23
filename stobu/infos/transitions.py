"""Scene Transition data module."""

# Official Libraries


# My Modules
from stobu.infos.common import get_record_as_splitter
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import SceneInfo
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'scene_transition_data_from',
        )


# Define Constants
PROC = 'INFO SCENE TRANSITION'


# Main
def scene_transition_data_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    cache = SceneInfo()

    tmp.append(get_record_as_splitter())
    tmp.append(InfoRecord(
        InfoType.DATA_TITLE, ActType.DATA, '## SCENE TRANSITIONS', '', ''))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.SCENE_HEAD is record.type:
            tmp.append(_record_of_scene_transition_from(record, cache))
            tmp.append(
                    InfoRecord(InfoType.SCENE_TRANSITION, record.act,
                        record.subject, record.outline, record.note))
            cache = record.note
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_transition_split())
        elif InfoType.TITLE_SCENE is record.type:
            continue
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return InfosData(tmp)


# Private Functions
def _get_record_as_transition_split() -> InfoRecord:
    line = '---'
    info = SceneInfo(line, line, line, line, line)

    return InfoRecord(InfoType.SCENE_TRANSITION, ActType.DATA, '', '', info)


def _record_of_scene_transition_from(record: InfoRecord,
        cache: SceneInfo) -> InfoRecord:
    assert isinstance(record, InfoRecord)
    assert isinstance(cache, SceneInfo)

    def _diff(a: str, b: str) -> str:
        if a != b:
            return '↓'
        else:
            return '…'

    base = assertion.is_instance(record.note, SceneInfo)

    dif = SceneInfo()

    dif.camera = _diff(base.camera, cache.camera)
    dif.stage = _diff(base.stage, cache.stage)
    dif.year = _diff(base.year, cache.year)
    dif.date = _diff(base.date, cache.date)
    dif.time = _diff(base.time, cache.time)

    return InfoRecord(InfoType.SCENE_TRANSITION, ActType.DATA, '', '', dif)
