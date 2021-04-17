"""Common count module."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.types.build import BuildType
from stobu.types.count import CountRecord, CountsData
from stobu.types.element import ElmType
from stobu.types.output import OutputsData
from stobu.utils.log import logger
from stobu.utils.strings import rid_rn


__all__ = (
        'counts_data_from',
        'count_line_by_columns',
        'count_white_space',
        )


# Define Constants
PROC = 'COMMON COUNTS'


NOVEL_BUILDS = [
        BuildType.NOVEL,
        BuildType.SCRIPT,
        ]


NOVEL_HEADS = {
        ElmType.BOOK: '# ',
        ElmType.CHAPTER: '## ',
        ElmType.EPISODE: '### ',
        ElmType.SCENE: '** ',
        }


OUTLINE_HEADS = {
        ElmType.BOOK: '### BOOK: ',
        ElmType.CHAPTER: '### CHAPTER: ',
        ElmType.EPISODE: '### EPISODE: ',
        ElmType.SCENE: '**',
        }


# Main
def counts_data_from(build_type: BuildType, outputs_data: OutputsData,
        columns: int, rows: int) -> CountsData:
    assert isinstance(build_type, BuildType)
    assert isinstance(outputs_data, OutputsData)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    _PROC = f"{PROC}: counts data"
    logger.debug(msg.PROC_START.format(proc=_PROC))

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

    heads = NOVEL_HEADS if build_type in NOVEL_BUILDS else OUTLINE_HEADS

    for record in outputs_data.get_data():
        assert isinstance(record, str)
        if record.startswith(heads[ElmType.BOOK]):
            indexes[ElmType.BOOK] += 1
            titles[ElmType.BOOK].append(_get_title_from(heads, ElmType.BOOK, record))
            descs[ElmType.BOOK].append('')
        elif record.startswith(heads[ElmType.CHAPTER]):
            indexes[ElmType.CHAPTER] += 1
            titles[ElmType.CHAPTER].append(_get_title_from(heads, ElmType.CHAPTER, record))
            descs[ElmType.CHAPTER].append('')
        elif record.startswith(heads[ElmType.EPISODE]):
            indexes[ElmType.EPISODE] += 1
            titles[ElmType.EPISODE].append(_get_title_from(heads, ElmType.EPISODE, record))
            descs[ElmType.EPISODE].append('')
        elif record.startswith(heads[ElmType.SCENE]):
            indexes[ElmType.SCENE] += 1
            titles[ElmType.SCENE].append(_get_title_from(heads, ElmType.SCENE, record))
            descs[ElmType.SCENE].append('')
        elif '<!--' in record:
            # NOTE: コメント
            continue
        else:
            # Text (Contains Spin)
            descs[ElmType.BOOK][indexes[ElmType.BOOK]] += record
            descs[ElmType.CHAPTER][indexes[ElmType.CHAPTER]] += record
            descs[ElmType.EPISODE][indexes[ElmType.EPISODE]] += record
            descs[ElmType.SCENE][indexes[ElmType.SCENE]] += record

    is_plot = BuildType.PLOT is build_type

    for elm in [ElmType.BOOK, ElmType.CHAPTER, ElmType.EPISODE, ElmType.SCENE]:
        tmp.extend(_counts_data_from_by_elm(elm, titles[elm], descs[elm], columns, rows, is_plot))

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return CountsData(tmp)


def count_line_by_columns(text: str, columns: int) -> float:
    assert isinstance(text, str)
    assert isinstance(columns, int)

    lines = text.split('\n')
    num = 0.0
    for line in lines:
        if len(line) > columns:
            num += len(line) / columns
        else:
            num += 1
    return num


def count_white_space(text: str) -> int:
    assert isinstance(text, str)

    space = 0
    for c in text:
        if c.isspace():
            space += 1
    return space


# Private Functions
def _counts_data_from_by_elm(elm: ElmType, titles: list, descs: list,
        columns: int, rows: int, is_rid_plotmark: bool) -> list:
    assert isinstance(elm, ElmType)
    assert isinstance(titles, list)
    assert isinstance(descs, list)
    assert isinstance(rows, int)
    assert isinstance(is_rid_plotmark, bool)

    tmp = []

    for title, text in zip(titles[1:], descs[1:]):
        _text = _rid_plot_mark(text) if is_rid_plotmark else text
        tmp.append(_record_count_from(elm, title, _text, columns, rows))

    return tmp


def _get_title_from(heads: dict, elm: ElmType, line: str) -> str:
    assert isinstance(heads, dict)
    assert isinstance(elm, ElmType)
    assert isinstance(line, str)

    if ElmType.SCENE is elm:
        return rid_rn(line.replace(heads[elm], '').replace(' **', ''))
    else:
        return rid_rn(line.replace(heads[elm], ''))


def _record_count_from(elm: ElmType, title: str, text: str,
        columns: int, rows: int) -> CountRecord:
    assert isinstance(elm, ElmType)
    assert isinstance(title, str)
    assert isinstance(text, str)
    assert isinstance(columns, int)
    assert isinstance(rows, int)

    lines = count_line_by_columns(text, columns)

    return CountRecord(
            elm,
            title,
            len(text),
            count_white_space(text),
            lines,
            lines / rows,
            )


def _rid_plot_mark(text: str) -> str:
    assert isinstance(text, str)

    return text.replace('→', '').replace('↓', '').replace('＜', '').replace('＞', '')
