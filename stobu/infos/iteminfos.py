"""Item info module."""

# Official Libraries


# My Modules
from stobu.infos.common import get_record_as_data_title, get_record_as_splitter
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import ItemInfo, ItemInfoType
from stobu.utils.log import logger


__all__ = (
        'item_infos_from',
        )


# Define Constants
PROC = 'INFO ITEM'


# Main
def item_infos_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    index = 0

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title('ITEM INFOS'))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_item_info_from(index, record)
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
    return InfoRecord(InfoType.ITEM_INFO, ActType.DATA, '', '',
            ItemInfo(ItemInfoType.NONE, -1, '', '', ''))


def _record_as_item_info_from(index: int, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(record, InfoRecord)

    info_type = ItemInfoType.NONE

    if ActType.HAVE is record.act:
        info_type = ItemInfoType.HAVE
    elif ActType.DISCARD is record.act:
        info_type = ItemInfoType.DISCARD
    else:
        return None

    return InfoRecord(InfoType.ITEM_INFO, record.act, record.subject, record.outline,
            ItemInfo(info_type, index, record.subject, record.outline, record.note))
