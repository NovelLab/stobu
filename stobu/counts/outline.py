"""Count module for outline data."""

# Official Libraries


# My Modules
from stobu.counts.common import count_line_by_columns, count_white_space
from stobu.syss import messages as msg
from stobu.types.count import CountsData, CountRecord
from stobu.types.element import ElmType
from stobu.types.output import OutputsData
from stobu.utils.log import logger
from stobu.utils.strings import rid_rn


__all__ = (
        'counts_data_from_outlines_outputs_data',
        )


# Define Constants
PROC = 'COUNT OUTLINES'


HEADS = {
        ElmType.BOOK: '### BOOK: ',
        ElmType.CHAPTER: '### CHAPTER: ',
        ElmType.EPISODE: '### EPISODE: ',
        ElmType.SCENE: '**',
        }


# Main
def counts_data_from_outlines_outputs_data(outputs_data: OutputsData,
        rows: int) -> CountsData:
    assert isinstance(outputs_data, OutputsData)
    assert isinstance(rows, int)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []

    indexes = {
            ElmType.BOOK: 0,
            ElmType.CHAPTER: 0,
            ElmType.EPISODE: 0,
            ElmType.SCENE: 0,
            }
    titles = {
            ElmType.BOOK: [""],
            ElmType.CHAPTER: [""],
            ElmType.EPISODE: [""],
            ElmType.SCENE: [""],
            }
    descs = {
            ElmType.BOOK: [""],
            ElmType.CHAPTER: [""],
            ElmType.EPISODE: [""],
            ElmType.SCENE: [""],
            }

    for record in outputs_data.get_data():
        assert isinstance(record, str)
        if record.startswith(HEADS[ElmType.BOOK]):
            indexes[ElmType.BOOK] += 1
            titles[ElmType.BOOK].append(_get_title_from(ElmType.BOOK, record))
            descs[ElmType.BOOK].append('')
        elif record.startswith(HEADS[ElmType.CHAPTER]):
            indexes[ElmType.CHAPTER] += 1
            titles[ElmType.CHAPTER].append(_get_title_from(ElmType.CHAPTER, record))
            descs[ElmType.CHAPTER].append('')
        elif record.startswith(HEADS[ElmType.EPISODE]):
            indexes[ElmType.EPISODE] += 1
            titles[ElmType.EPISODE].append(_get_title_from(ElmType.EPISODE, record))
            descs[ElmType.EPISODE].append('')
        elif record.startswith(HEADS[ElmType.SCENE]):
            indexes[ElmType.SCENE] += 1
            titles[ElmType.SCENE].append(_get_title_from(ElmType.SCENE, record))
            descs[ElmType.SCENE].append('')
        elif record.startswith('<!--'):
            # NOTE: コメントを含むか否か
            continue
        else:
            # Text
            descs[ElmType.BOOK][indexes[ElmType.BOOK]] += record
            descs[ElmType.CHAPTER][indexes[ElmType.CHAPTER]] += record
            descs[ElmType.EPISODE][indexes[ElmType.EPISODE]] += record
            descs[ElmType.SCENE][indexes[ElmType.SCENE]] += record

    for elm in [ElmType.BOOK, ElmType.CHAPTER, ElmType.EPISODE, ElmType.SCENE]:
        tmp.extend(_counts_data_from_by_elm(elm, titles[elm], descs[elm], rows))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return CountsData(tmp)


# Private Functions
def _counts_data_from_by_elm(elm: ElmType, titles: list, descs: list,
        rows: int) -> list:
    assert isinstance(elm, ElmType)
    assert isinstance(titles, list)
    assert isinstance(descs, list)
    assert isinstance(rows, int)

    tmp = []

    for title, text in zip(titles[1:], descs[1:]):
        tmp.append(_record_count_from(elm, title, text, rows))

    return tmp


def _get_title_from(elm: ElmType, line: str) -> str:
    assert isinstance(elm, ElmType)
    assert isinstance(line, str)

    return rid_rn(line.replace(HEADS[elm], ''))


def _record_count_from(elm: ElmType, title: str, text: str, rows: int) -> CountRecord:
    assert isinstance(elm, ElmType)
    assert isinstance(title, str)
    assert isinstance(text, str)
    assert isinstance(rows, int)

    lines = count_line_by_columns(text, rows)

    return CountRecord(
            elm,
            title,
            len(text),
            count_white_space(text),
            lines,
            lines / rows,
            )
