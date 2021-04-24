"""Persons info data module."""

# Official Libraries


# My Modules
from stobu.infos.common import get_record_as_splitter, get_record_as_data_title
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import PersonInfo, PersonInfoType
from stobu.utils.log import logger


__all__ = (
        'person_infos_from',
        )


# Define Constants
PROC = 'INFO PERSONS'


# Main
def person_infos_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    index = 0

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title('PERSON INFOS'))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_person_info_from(index, record)
            if ret:
                tmp.append(ret)
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_data_splitter())
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return InfosData(tmp)


# Private Functions
def _get_record_as_data_splitter() -> InfoRecord:
    return InfoRecord(InfoType.PERSON_INFO, ActType.DATA, '', '',
            PersonInfo(PersonInfoType.NONE, 0, '', ''))


def _record_as_person_info_from(index: int, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(record, InfoRecord)

    info_type = PersonInfoType.NONE

    if ActType.BE is record.act:
        info_type = PersonInfoType.BE
    elif ActType.COME is record.act:
        info_type = PersonInfoType.COME
    elif ActType.GO is record.act:
        info_type = PersonInfoType.GO
    else:
        return None

    info = PersonInfo(info_type, index, record.subject, record.outline)

    return InfoRecord(InfoType.PERSON_INFO, record.act, record.subject, record.outline,
            info)
