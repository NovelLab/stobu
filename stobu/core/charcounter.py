"""Counter module for storybuilder project."""


# Official Libraries


# My Modules
from stobu.core.novelbuilder import get_story_code_data_from_story_data_as_novel
from stobu.core.outlinebuilder import get_outline_data
from stobu.core.plotbuilder import get_plot_data
from stobu.core.scriptbuilder import get_story_code_data_from_story_data_as_script
from stobu.dataconverter import conv_text_from_tag, conv_text_list_by_tags
from stobu.datatypes import CountData, CountRecord
from stobu.datatypes import OutlineData, OutlineRecord
from stobu.datatypes import OutputData
from stobu.datatypes import PlotData, PlotRecord
from stobu.datatypes import StoryCodeData
from stobu.datatypes import StoryData
from stobu.formatter import format_charcounts_novel, format_charcounts_outline, format_charcounts_plot, format_charcounts_script, format_novel_data, format_script_data
from stobu import projectpathmanager as ppath
from stobu.util import assertion
from stobu.util.counttool import count_white_space, count_line_by_columns
from stobu.util.fileio import read_file_as_yaml
from stobu.util.log import logger


__all__ = (
        'on_build_novel_charcounts',
        'on_build_outline_charcounts',
        'on_build_plot_charcounts',
        'on_build_script_charcounts',
        )


# Main Functions
def on_build_novel_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    story_code_data = assertion.is_instance(
            get_story_code_data_from_story_data_as_novel(story_data, tags), StoryCodeData)

    novels = format_novel_data(story_code_data)

    novels_fixed = conv_text_list_by_tags(novels, tags)

    rows, columns = _get_rows_and_columns_from_bookdata()

    novelcounts = assertion.is_instance(
            _get_novel_char_counts(novels_fixed, rows, columns),
            CountData)

    output_data = format_charcounts_novel(novelcounts)

    return OutputData(output_data)


def on_build_outline_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    rows, columns = _get_rows_and_columns_from_bookdata()

    outlines = _get_outline_char_counts('book', story_data, tags, rows, columns) \
            + _get_outline_char_counts('chapter', story_data, tags, rows, columns) \
            + _get_outline_char_counts('episode', story_data, tags, rows, columns) \
            + _get_outline_char_counts('scene', story_data, tags, rows, columns)

    output_data = format_charcounts_outline(outlines)

    return OutputData(output_data)


def on_build_plot_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    rows, columns = _get_rows_and_columns_from_bookdata()

    plots = _get_plot_char_counts('book', story_data, tags, rows, columns) \
            + _get_plot_char_counts('chapter', story_data, tags, rows, columns) \
            + _get_plot_char_counts('episode', story_data, tags, rows, columns) \
            + _get_plot_char_counts('scene', story_data, tags, rows, columns)

    output_data = format_charcounts_plot(plots)

    return OutputData(output_data)


def on_build_script_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    story_code_data = assertion.is_instance(
            get_story_code_data_from_story_data_as_script(story_data, tags), StoryCodeData)

    scripts = format_script_data(story_code_data, tags)

    scripts_fixed = conv_text_list_by_tags(scripts, tags)

    rows, columns = _get_rows_and_columns_from_bookdata()

    scriptcounts = assertion.is_instance(
            _get_script_char_counts(scripts_fixed, rows, columns),
            CountData)

    output_data = format_charcounts_script(scriptcounts)

    return OutputData(output_data)


# Private Functions
def _get_count_record_end(level: str) -> CountRecord:
    assert isinstance(level, str)

    return CountRecord(level, '_end', 0, 0, 0.0, 0.0)


def _get_count_record_head(level: str) -> CountRecord:
    assert isinstance(level, str)

    return CountRecord(level, '_head', 0, 0, 0.0, 0.0)


def _get_novel_char_counts(formatted: list, rows: int, columns: int) -> CountData:
    assert isinstance(formatted, list)
    assert isinstance(rows, int)
    assert isinstance(columns, int)

    tmp = []

    books = [""]
    chapters = [""]
    episodes = [""]
    scenes = [""]
    book_titles = [""]
    ch_titles = [""]
    ep_titles = [""]
    sc_titles = [""]
    book_idx, ch_idx, ep_idx, sc_idx = 0, 0, 0, 0

    for line in formatted:
        assert isinstance(line, str)
        if line.startswith('# '):
            # Book title
            book_idx += 1
            books.append("")
            book_titles.append(line[2:].rstrip('\n\r'))
        elif line.startswith('## '):
            # Chapter title
            ch_idx += 1
            chapters.append("")
            ch_titles.append(line[3:].rstrip('\n\r'))
        elif line.startswith('### '):
            # Episode title
            ep_idx += 1
            episodes.append("")
            ep_titles.append(line[4:].rstrip('\n\r'))
        elif line.startswith('**'):
            # Scene title
            sc_idx += 1
            scenes.append("")
            sc_titles.append(line.replace('**', '').rstrip('\n\r'))
        else:
            # Text
            books[book_idx] += line
            chapters[ch_idx] += line
            episodes[ep_idx] += line
            scenes[sc_idx] += line

    book_idx = 1
    tmp.append(_get_count_record_head('book'))
    for book, title in zip(books[1:], book_titles[1:]):
        text = books[book_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('book', title, len(text),
            count_white_space(text), lines, lines / rows))
        book_idx += 1
    tmp.append(_get_count_record_end('book'))

    ch_idx = 1
    tmp.append(_get_count_record_head('chapter'))
    for chapter, title in zip(chapters[1:], ch_titles[1:]):
        text = chapters[ch_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('chapter', title, len(text),
            count_white_space(text), lines, lines / rows))
        ch_idx += 1
    tmp.append(_get_count_record_end('chapter'))

    ep_idx = 1
    tmp.append(_get_count_record_head('episode'))
    for episode, title in zip(episodes[1:], ep_titles[1:]):
        text = episodes[ep_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('episode', title, len(text),
            count_white_space(text), lines, lines / rows))
        ep_idx += 1
    tmp.append(_get_count_record_end('episode'))

    sc_idx = 1
    tmp.append(_get_count_record_head('scene'))
    for scene, title in zip(scenes[1:], sc_titles[1:]):
        text = scenes[sc_idx]
        lines = count_line_by_columns(text, rows)
        tmp.append(CountRecord('scene', title, len(text),
            count_white_space(text), lines, lines / rows))
        sc_idx += 1
    tmp.append(_get_count_record_end('scene'))

    return CountData(tmp)


def _get_outline_char_counts(level: str, story_data: StoryData, tags: dict,
        rows: int, columns: int) -> CountData:
    assert isinstance(level, str)
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(rows, int)
    assert isinstance(columns, int)

    outline_data = assertion.is_instance(get_outline_data(level, story_data),
            OutlineData)
    tmp = []
    full_text = ""

    for record in outline_data.get_data():
        assert isinstance(record, OutlineRecord)
        text = conv_text_from_tag(record.data, tags)
        lines = count_line_by_columns(text, columns)
        tmp.append(
                CountRecord(level,
                    record.title,
                    len(text),
                    count_white_space(text),
                    lines,
                    lines /rows,
                    ))
        full_text += text
    full_lines = count_line_by_columns(full_text, columns)
    totalcount = CountRecord(level, "_head",
            sum([r.total for r in tmp]),
            count_white_space(full_text),
            full_lines,
            full_lines / rows,
            )

    return CountData([totalcount] + tmp + [_get_count_record_end(level)])


def _get_plot_char_counts(level: str, story_data: StoryData, tags: dict,
        rows: int, columns: int) -> CountData:
    assert isinstance(level, str)
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)
    assert isinstance(rows, int)
    assert isinstance(columns, int)

    plot_data = assertion.is_instance(get_plot_data(level, story_data), PlotData)

    tmp = []
    full_text = ""
    for record in plot_data.get_data():
        assert isinstance(record, PlotRecord)
        text = record.setup + record.tp1st + record.develop + record.tp2nd + record.climax + record.resolve
        text_fixed = conv_text_from_tag(text, tags)
        lines = count_line_by_columns(text_fixed, columns)
        tmp.append(CountRecord(level,
            record.title,
            len(text_fixed),
            count_white_space(text_fixed),
            lines,
            lines / rows))
        full_text += text_fixed
    full_lines = count_line_by_columns(full_text, columns)
    totalcount = CountRecord(level, "_head", sum([r.total for r in tmp]),
            count_white_space(full_text),
            full_lines,
            full_lines / rows)

    return CountData([totalcount] + tmp + [_get_count_record_end(level)])


def _get_rows_and_columns_from_bookdata() -> tuple:
    bookdata = assertion.is_dict(read_file_as_yaml(ppath.get_book_path()))

    return (bookdata['rows'], bookdata['columns'])


def _get_script_char_counts(formatted: list, rows: int, columns: int) -> CountData:
    assert isinstance(formatted, list)
    assert isinstance(rows, int)
    assert isinstance(columns, int)

    tmp = []

    books = [""]
    chapters = [""]
    episodes = [""]
    scenes = [""]
    book_titles = [""]
    ch_titles = [""]
    ep_titles = [""]
    sc_titles = [""]
    book_idx, ch_idx, ep_idx, sc_idx = 0, 0, 0, 0

    for line in formatted:
        assert isinstance(line, str)
        if line.startswith('# '):
            # Book title
            book_idx += 1
            books.append("")
            book_titles.append(line[2:].rstrip('\n\r'))
        elif line.startswith('## '):
            # Chapter title
            ch_idx += 1
            chapters.append("")
            ch_titles.append(line[3:].rstrip('\n\r'))
        elif line.startswith('### '):
            # Episode title
            ep_idx += 1
            episodes.append("")
            ep_titles.append(line[4:].rstrip('\n\r'))
        elif line.startswith('**'):
            # Scene title
            sc_idx += 1
            scenes.append("")
            sc_titles.append(line.replace('**', '').rstrip('\n\r'))
        elif line.startswith('○　'):
            # Spin
            pass
        else:
            # Text
            books[book_idx] += line
            chapters[ch_idx] += line
            episodes[ep_idx] += line
            scenes[sc_idx] += line

    book_idx = 1
    tmp.append(_get_count_record_head('book'))
    for book, title in zip(books[1:], book_titles[1:]):
        text = books[book_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('book', title, len(text),
            count_white_space(text), lines, lines / rows))
        book_idx += 1
    tmp.append(_get_count_record_end('book'))

    ch_idx = 1
    tmp.append(_get_count_record_head('chapter'))
    for chapter, title in zip(chapters[1:], ch_titles[1:]):
        text = chapters[ch_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('chapter', title, len(text),
            count_white_space(text), lines, lines / rows))
        ch_idx += 1
    tmp.append(_get_count_record_end('chapter'))

    ep_idx = 1
    tmp.append(_get_count_record_head('episode'))
    for episode, title in zip(episodes[1:], ep_titles[1:]):
        text = episodes[ep_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('episode', title, len(text),
            count_white_space(text), lines, lines / rows))
        ep_idx += 1
    tmp.append(_get_count_record_end('episode'))

    sc_idx = 1
    tmp.append(_get_count_record_head('scene'))
    for scene, title in zip(scenes[1:], sc_titles[1:]):
        text = scenes[sc_idx]
        lines = count_line_by_columns(text, columns)
        tmp.append(CountRecord('scene', title, len(text),
            count_white_space(text), lines, lines / rows))
        sc_idx += 1
    tmp.append(_get_count_record_end('scene'))

    return CountData(tmp)
