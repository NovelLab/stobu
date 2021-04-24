"""Fashion info data module."""

# Official Libraries


# My Modules
from stobu.infos.common import get_record_as_data_title, get_record_as_splitter
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import FashionInfo
from stobu.utils.log import logger


__all__ = (
        'fashion_infos_from',
        )


# Define Constants
PROC = 'INFO FASHION'


# Main
def fashion_infos_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    index = 0

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title('FASHIN INFOS'))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_fashion_info_from(index, record)
            if ret:
                tmp.append(ret)
        elif InfoType.TITLE_EPISODE is record.type:
            tmp.append(_get_record_as_splitter())
        elif InfoType.TITLE_SCENE is record.type:
            index += 1
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return InfosData(tmp)


# Private Functions
def _get_record_as_splitter() -> InfoRecord:
    return InfoRecord(InfoType.FASHION_INFO, ActType.DATA, '', '',
            FashionInfo(-1, '----', '----'))


def _record_as_fashion_info_from(index: int, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(record, InfoRecord)

    if ActType.WEAR is record.act:
        info = FashionInfo(index, record.subject, record.outline, record.note)
        return InfoRecord(InfoType.FASHION_INFO, record.act, record.subject,
                record.outline, info)
    else:
        return None
