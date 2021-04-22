"""Flag info collection module."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import FlagInfo, FlagType
from stobu.utils.log import logger


__all__ = (
        'flag_infos_from',
        )


# Define Constants
PROC = 'INFO FLAGS'


# Main
def flag_infos_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    index = 0

    tmp.append(_get_record_as_splitter())
    tmp.append(InfoRecord(
        InfoType.DATA_TITLE, ActType.DATA, '## SCENE FLAG INFOS', '', ''))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            continue
        elif InfoType.FLAG_FORESHADOW is record.type:
            tmp.append(_record_as_flag_info_from(record, index, FlagType.FLAG))
        elif InfoType.FLAG_PAYOFF is record.type:
            tmp.append(_record_as_flag_info_from(record, index, FlagType.DEFLAG))
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_flag_info_split())
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return InfosData(tmp)


# Private Functions
def _get_record_as_flag_info_split() -> InfoRecord:
    info = FlagInfo(FlagType.NONE, 0, '', '', '')

    return InfoRecord(InfoType.FLAG_INFO, ActType.DATA, '', '', info)


def _get_record_as_splitter() -> InfoRecord:
    return InfoRecord(InfoType.SPLITTER, ActType.DATA, '', '', '')


def _record_as_flag_info_from(record: InfoRecord, index: int,
        flag_type: FlagType) -> InfoRecord:
    assert isinstance(record, InfoRecord)
    assert isinstance(index, int)
    assert isinstance(flag_type, FlagType)

    return InfoRecord(
            InfoType.FLAG_INFO,
            ActType.DATA,
            '', '',
            FlagInfo(flag_type, index, record.subject, record.outline, record.note))
