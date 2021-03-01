"""Format module for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.dataconverter import conv_text_from_tag
from storybuilder.datatypes import ContentRecord, OutlineRecord, PlotRecord, StoryCode
from storybuilder.util.log import logger


__all__ = (
        'format_contents_table_data',
        'format_novel_data',
        'format_outline_data',
        'format_plot_data',
        'format_script_data',
        'get_breakline',
        )


# Main Functions
def format_contents_table_data(contents: list) -> list:
    assert isinstance(contents, list)

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


def format_novel_data(code_data: list, indent_num: int=1) -> list:
    assert isinstance(code_data, list)
    assert isinstance(indent_num, int)

    tmp = []

    for code in code_data:
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


def format_outline_data(level: str, outlines: list) -> list:
    assert isinstance(level, str)
    assert isinstance(outlines, list)

    tmp = []

    tmp.append(_get_head_by_level(level))

    for record in outlines:
        assert isinstance(record, OutlineRecord)
        tmp.append(f"**{record.title}**\n")
        tmp.append(f"    {record.data}\n\n")
    return tmp


def format_plot_data(level: str, plots: list) -> list:
    assert isinstance(level, str)
    assert isinstance(plots, list)

    tmp = []

    tmp.append(_get_head_by_level(level))

    for record in plots:
        assert isinstance(record, PlotRecord)
        tmp.append(f"**{record.title}**\n")
        tmp.append(f"    {record.setup}\n")
        tmp.append(f"    ↓＜{record.tp1st}\n")
        tmp.append(f"    {record.develop}\n")
        tmp.append(f"    ↓＜{record.tp2nd}\n")
        tmp.append(f"    {record.climax}\n")
        tmp.append(f"    ＞{record.resolve}\n")
    return tmp


def format_script_data(code_data: list, tags: dict, indent_num: int=3) -> list:
    assert isinstance(code_data, list)
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

    for code in code_data:
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
            tmp.append(f"○　{scene_data['stage']}（scene_data['time']）\n")
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
def _get_head_by_level(level: str) -> str:
    assert isinstance(level, str)

    if level == 'book':
        return "## BOOK outline\n\n"
    elif level == 'chapter':
        return "## CHAPTER outlines\n\n"
    elif level == 'episode':
        return "## EPISODE outlines\n\n"
    elif level == 'scene':
        return "## SCENE outlines\n\n"
    else:
        return "## outlines\n\n"
