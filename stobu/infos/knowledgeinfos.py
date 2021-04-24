"""Knowledge info data module."""

# Official Libraries


# My Modules
from stobu.infos.common import get_record_as_data_title, get_record_as_splitter
from stobu.syss import messages as msg
from stobu.types.action import ActType
from stobu.types.info import InfoRecord, InfosData, InfoType
from stobu.types.info import KnowledgeInfo, KnowledgeInfoType
from stobu.utils.log import logger


__all__ = (
        'knowledge_infos_from',
        )


# Define Constants
PROC = 'INFO KNOWLEDGE'


# Main
def knowledge_infos_from(infos_data: InfosData) -> InfosData:
    assert isinstance(infos_data, InfosData)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    index = 0

    tmp.append(get_record_as_splitter())
    tmp.append(get_record_as_data_title('KNOWLEDGE INFOS'))

    for record in infos_data.get_data():
        assert isinstance(record, InfoRecord)
        if InfoType.ACTION is record.type:
            ret = _record_as_knowledge_info_from(index, record)
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
    return InfoRecord(InfoType.KNOWLEDGE_INFO, ActType.DATA, '', '',
            KnowledgeInfo(KnowledgeInfoType.NONE, -1, '', '', ''))


def _record_as_knowledge_info_from(index: int, record: InfoRecord) -> InfoRecord:
    assert isinstance(index, int)
    assert isinstance(record, InfoRecord)

    info_type = KnowledgeInfoType.NONE

    if ActType.EXPLAIN is record.act:
        info_type = KnowledgeInfoType.EXPLAIN
    elif ActType.KNOW is record.act:
        info_type = KnowledgeInfoType.KNOW
    elif ActType.KNOWN is record.act:
        info_type = KnowledgeInfoType.KNOWN
    elif ActType.REMEMBER is record.act:
        info_type = KnowledgeInfoType.REMEMBER
    else:
        return None

    return InfoRecord(
            InfoType.KNOWLEDGE_INFO, ActType.DATA, record.subject, record.outline,
            KnowledgeInfo(info_type, index, record.subject, record.outline, record.note))
