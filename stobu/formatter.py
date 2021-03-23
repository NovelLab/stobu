"""Format module for storybuilder project."""


# Official Libraries


# My Modules
from stobu.dataconverter import conv_text_from_tag
from stobu.datatypes import CountData, CountRecord
from stobu.datatypes import ContentsData, ContentRecord
from stobu.datatypes import OutlineData, OutlineRecord
from stobu.datatypes import PlotData, PlotRecord
from stobu.datatypes import StoryCode, StoryCodeData
from stobu.util import assertion
from stobu.util.log import logger
from stobu.util.strings import just_string_of


__all__ = (
        'format_charcounts_outline',
        'format_charcounts_plot',
        'format_charcounts_script',
        'format_contents_table_data',
        'format_novel_data',
        'format_outline_data',
        'format_plot_data',
        'format_scene_info_data',
        'format_script_data',
        'get_breakline',
        )


# Main Functions
def format_charcounts_novel(novels: CountData) -> list:
    assert isinstance(novels, CountData)

    tmp = []
    tmp.append("## NOVEL count:\n\n")

    for record in novels.get_data():
        assert isinstance(record, CountRecord)
        if 'book' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('book', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
        elif 'chapter' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('chapter', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'episode' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('episode', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'scene' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('scene', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        else:
            logger.debug("Unknown CountRecord in script char counts!: %s", record)
            continue

    return tmp


def format_charcounts_outline(outlines: CountData) -> list:
    assert isinstance(outlines, CountData)

    tmp = []
    tmp.append("## OUTLINE count:\n\n")

    for record in outlines.get_data():
        assert isinstance(record, CountRecord)
        if 'book' == record.category:
            if '_head' == record.title:
                continue
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(_get_head_by_level('book', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'chapter' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('chapter', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'episode' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('episode', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'scene' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('scene', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        else:
            logger.debug("Unknown CountRecord in outline char counts!: %s", record)
            continue
    return tmp


def format_charcounts_plot(outlines: CountData) -> list:
    assert isinstance(outlines, CountData)

    tmp = []
    tmp.append("## PLOT count:\n\n")

    for record in outlines.get_data():
        assert isinstance(record, CountRecord)
        if 'book' == record.category:
            if '_head' == record.title:
                continue
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(_get_head_by_level('book', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'chapter' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('chapter', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'episode' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('episode', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'scene' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('scene', 'count'))
                tmp.append(f"{_get_charcounts_elemenet(record, 'total')}\n")
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        else:
            logger.debug("Unknown CountRecord in plot char counts!: %s", record)
            continue
    return tmp


def format_charcounts_script(scripts: CountData) -> list:
    assert isinstance(scripts, CountData)

    tmp = []
    tmp.append("## SCRIPT count:\n\n")

    for record in scripts.get_data():
        assert isinstance(record, CountRecord)
        if 'book' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('book', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'chapter' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('chapter', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'episode' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('episode', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        elif 'scene' == record.category:
            if '_head' == record.title:
                tmp.append(_get_head_by_level('scene', 'count'))
            elif '_end' == record.title:
                tmp.append('\n')
            else:
                tmp.append(f"{_get_charcounts_elemenet(record)}\n")
        else:
            logger.debug("Unknown CountRecord in script char counts!: %s", record)
            continue

    return tmp


def format_contents_table_data(contents_data: ContentsData) -> list:
    assert isinstance(contents_data, ContentsData)

    contents = contents_data.get_data()
    tmp = []
    tmp.append(f"{contents[0].title}\n")
    tmp.append("====\n\n")
    tmp.append("## CONTENTS\n\n")

    for record in contents[1:]:
        assert isinstance(record, ContentRecord)
        space = ""
        if record.category == 'chapter':
            space = ""
        elif record.category == 'episode':
            space = "    "
        elif record.category == 'scene':
            space = "    " * 2
        tmp.append(f"{space}{record.index}. {record.title}\n")
    return tmp


def format_novel_data(code_data: StoryCodeData, indent_num: int = 1) -> list:
    assert isinstance(code_data, StoryCodeData)
    assert isinstance(indent_num, int)

    tmp = []

    for code in code_data.get_data():
        assert isinstance(code, StoryCode)
        if 'book-title' == code.head:
            tmp.append(f"# {code.body}\n\n")
        elif 'chapter-title' == code.head:
            tmp.append(f"## {code.body}\n\n")
        elif 'episode-title' == code.head:
            tmp.append(f"### {code.body}\n\n")
        elif 'scene-title' == code.head:
            tmp.append(f"**{code.body}**\n\n")
        elif 'title' in code.head:
            tmp.append(f"{code.body}\n")
        elif code.head in ('scene-camera', 'scene-stage', 'scene-year', 'scene-date', 'scene-time'):
            continue
        elif 'scene-start' == code.head:
            continue
        elif 'scene-end' == code.head:
            tmp.append('\n')
        elif code.head in ('description', 'monologue'):
            suffix = "" if code.body.endswith(('。', '、')) else '。'
            tmp.append(f"{code.body}{suffix}")
        elif 'dialogue' == code.head:
            tmp.append(f"「{code.body}」")
        elif 'br' == code.head:
            tmp.append('\n')
        elif 'indent' == code.head:
            tmp.append('　' * indent_num)
        else:
            logger.debug("Unknown StoryCode!: %s", code)
            continue

    return tmp


def format_outline_data(level: str, outlines: OutlineData) -> list:
    assert isinstance(level, str)
    assert isinstance(outlines, OutlineData)

    tmp = []

    tmp.append(_get_head_by_level(level, 'outline'))

    for record in outlines.get_data():
        assert isinstance(record, OutlineRecord)
        tmp.append(f"**{record.title}**\n")
        tmp.append(f"    {record.data}\n\n")
    return tmp


def format_plot_data(level: str, plots: PlotData) -> list:
    assert isinstance(level, str)
    assert isinstance(plots, PlotData)

    tmp = []

    tmp.append(_get_head_by_level(level, 'plot'))

    for record in plots.get_data():
        assert isinstance(record, PlotRecord)
        tmp.append(f"**{record.title}**\n")
        tmp.append(f"    {record.setup}\n")
        tmp.append(f"    ↓＜{record.tp1st}\n")
        tmp.append(f"    {record.develop}\n")
        tmp.append(f"    ↓＜{record.tp2nd}\n")
        tmp.append(f"    {record.climax}\n")
        tmp.append(f"    ＞{record.resolve}\n")
    return tmp


def format_scene_info_data(code_data: StoryCodeData, tags: dict) -> list:
    assert isinstance(code_data, StoryCodeData)
    assert isinstance(tags, dict)

    tmp = []
    scene_data = {
            'camera': '',
            'stage': '',
            'year': '',
            'date': '',
            'time': '',
            }

    scn_idx = 0
    def info_format(stage: str, time: str, date: str, year: str, camera: str,
            use_bracket: bool = True) -> str:
        _stage = just_string_of(stage, 32)
        _time = just_string_of(time, 4)
        _date = just_string_of(date, 16)
        _year = just_string_of(year, 8)
        _camera = camera
        if use_bracket:
            return f"{_stage}（{_time}）｜{_date}/{_year}＜{_camera}＞"
        else:
            return f"{_stage}  {_time}    {_date} {_year}  {_camera}"
    for code in code_data.get_data():
        assert isinstance(code, StoryCode)

        if 'book-title' == code.head:
            tmp.append(f"# {code.body}\n\n")
        elif 'chapter-title' == code.head:
            tmp.append(f"## {code.body}\n\n")
        elif 'episode-title' == code.head:
            tmp.append(f"### {code.body}\n\n")
        elif 'scene-title' == code.head:
            continue
        elif 'scene-camera' == code.head:
            scene_data['camera'] = code.body
        elif 'scene-stage' == code.head:
            scene_data['stage'] = code.body
        elif 'scene-year' == code.head:
            scene_data['year'] = code.body
        elif 'scene-date' == code.head:
            scene_data['date'] = code.body
        elif 'scene-time' == code.head:
            scene_data['time'] = code.body
        elif 'scene-start' == code.head:
            camera = scene_data['camera']
            stage = scene_data['stage']
            year = scene_data['year']
            date = scene_data['date']
            time = scene_data['time']
            tmp.append(f"{scn_idx:4}. {info_format(stage, time, date, year, camera)}\n")
            scn_idx += 1
        elif 'scene-end' == code.head:
            continue
        elif 'scene-elapsed' == code.head:
            elapsed = assertion.is_dict(code.foot)
            stage = '↓' if elapsed['stage'] == 'changed' else '…'
            time = '↓' if elapsed['time'] == 'changed' else '…'
            date = '↓' if elapsed['date'] == 'changed' else '…'
            year = '↓' if elapsed['year'] == 'changed' else '…'
            camera = '↓' if elapsed['camera'] == 'changed' else '…'
            tmp.insert(-1, f"      {info_format(stage, time, date, year, camera, False)}\n")
        else:
            continue
    return tmp


def format_script_data(code_data: StoryCodeData, tags: dict, indent_num: int = 3) -> list:
    assert isinstance(code_data, StoryCodeData)
    assert isinstance(tags, dict)
    assert isinstance(indent_num, int)

    tmp = []
    scene_data = {
            'camera': "",
            'stage': "",
            'year': "",
            'date': "",
            'time': "",
            }

    for code in code_data.get_data():
        assert isinstance(code, StoryCode)
        if 'book-title' == code.head:
            tmp.append(f"# {code.body}\n\n")
        elif 'chapter-title' == code.head:
            tmp.append(f"## {code.body}\n\n")
        elif 'episode-title' == code.head:
            tmp.append(f"### {code.body}\n\n")
        elif 'scene-title' == code.head:
            tmp.append(f"**{code.body}**\n\n")
        elif 'title' in code.head:
            tmp.append(f"{code.body}\n")
        elif 'scene-camera' == code.head:
            scene_data['camera'] = code.body
        elif 'scene-stage' == code.head:
            scene_data['stage'] = code.body
        elif 'scene-year' == code.head:
            scene_data['year'] = code.body
        elif 'scene-date' == code.head:
            scene_data['date'] = code.body
        elif 'scene-time' == code.head:
            scene_data['time'] = code.body
        elif 'scene-start' == code.head:
            tmp.append(f"○　{scene_data['stage']}（{scene_data['time']}）\n")
        elif 'scene-end' == code.head:
            tmp.append('\n')
        elif 'description' == code.head:
            suffix = "" if code.body.endswith(('。', '、')) else '。'
            tmp.append(f"{code.body}{suffix}")
        elif 'dialogue' == code.head:
            subject = conv_text_from_tag(code.foot, tags, "")
            tmp.append(f"{subject}「{code.body}」")
        elif 'monologue' == code.head:
            subject = conv_text_from_tag(code.foot, tags, "")
            tmp.append(f"{subject}Ｍ『{code.body}』")
        elif 'br' == code.head:
            tmp.append('\n')
        elif 'indent' == code.head:
            tmp.append('　' * indent_num)
        else:
            logger.debug("Unknown StoryCode!: %s", code)
            continue

    return tmp


def get_breakline() -> str:
    return "--------" * 8 + "\n"


# Private Functions
def _get_head_by_level(level: str, title: str) -> str:
    assert isinstance(level, str)
    assert isinstance(title, str)

    if level == 'book':
        return f"### BOOK {title}\n\n"
    elif level == 'chapter':
        return f"### CHAPTER {title}\n\n"
    elif level == 'episode':
        return f"### EPISODE {title}\n\n"
    elif level == 'scene':
        return f"### SCENE {title}\n\n"
    else:
        return f"### {title}\n\n"


def _get_charcounts_elemenet(record: CountRecord, title: str = None) -> str:
    assert isinstance(record, CountRecord)

    title = assertion.is_str(title) if title else record.title
    total = record.total
    space = record.space
    real = total - space
    lines = round(record.lines, 3)
    papers = round(record.papers, 3)

    return f"- {just_string_of(title, 16)}: {papers}p/{lines}n [{total}c ({real}/{space})c]"
