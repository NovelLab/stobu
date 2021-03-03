"""Counter module for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.core.novelbuilder import get_story_code_data_from_story_data_as_novel
from storybuilder.core.outlinebuilder import get_outline_data
from storybuilder.core.plotbuilder import get_plot_data
from storybuilder.core.scriptbuilder import get_story_code_data_from_story_data_as_script
from storybuilder.dataconverter import conv_text_from_tag, conv_text_list_by_tags
from storybuilder.datatypes import CountData, CountRecord
from storybuilder.datatypes import OutlineData, OutlineRecord
from storybuilder.datatypes import OutputData
from storybuilder.datatypes import PlotData, PlotRecord
from storybuilder.datatypes import StoryCodeData
from storybuilder.datatypes import StoryData
from storybuilder.formatter import format_charcounts_novel, format_charcounts_outline, format_charcounts_plot, format_charcounts_script, format_novel_data, format_script_data
from storybuilder.projectcounter import get_charcounts_novel_data, get_charcounts_script_data
from storybuilder.util import assertion
from storybuilder.util.log import logger


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

    novelcounts = assertion.is_instance(get_charcounts_novel_data(novels_fixed),
            CountData)

    output_data = format_charcounts_novel(novelcounts)

    return OutputData(output_data)


def on_build_outline_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    outlines = _get_outline_char_counts('book', story_data, tags) \
            + _get_outline_char_counts('chapter', story_data, tags) \
            + _get_outline_char_counts('episode', story_data, tags) \
            + _get_outline_char_counts('scene', story_data, tags)

    output_data = format_charcounts_outline(outlines)

    return OutputData(output_data)


def on_build_plot_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    plots = _get_plot_char_counts('book', story_data, tags) \
            + _get_plot_char_counts('chapter', story_data, tags) \
            + _get_plot_char_counts('episode', story_data, tags) \
            + _get_plot_char_counts('scene', story_data, tags)

    output_data = format_charcounts_plot(plots)

    return OutputData(output_data)


def on_build_script_charcounts(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    story_code_data = assertion.is_instance(
            get_story_code_data_from_story_data_as_script(story_data, tags), StoryCodeData)

    scripts = format_script_data(story_code_data, tags)

    scripts_fixed = conv_text_list_by_tags(scripts, tags)

    scriptcounts = assertion.is_instance(get_charcounts_script_data(scripts_fixed),
            CountData)

    output_data = format_charcounts_script(scriptcounts)

    return OutputData(output_data)


# Private Functions
def _get_outline_char_counts(level: str, story_data: StoryData, tags: dict) -> CountData:
    assert isinstance(level, str)
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    outline_data = assertion.is_instance(get_outline_data(level, story_data),
            OutlineData)
    tmp = []

    for record in outline_data.get_data():
        assert isinstance(record, OutlineRecord)
        text = conv_text_from_tag(record.data, tags)
        tmp.append(CountRecord(level, record.title, len(text)))
    totalcount = CountRecord(level, "_head", sum([r.total for r in tmp]))

    return CountData([totalcount] + tmp + [CountRecord(level, "_end", 0)])


def _get_plot_char_counts(level: str, story_data: StoryData, tags: dict) -> CountData:
    assert isinstance(level, str)
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    plot_data = assertion.is_instance(get_plot_data(level, story_data), PlotData)

    tmp = []
    for record in plot_data.get_data():
        assert isinstance(record, PlotRecord)
        text = record.setup + record.tp1st + record.develop + record.tp2nd + record.climax + record.resolve
        text_fixed = conv_text_from_tag(text, tags)
        tmp.append(CountRecord(level, record.title, len(text_fixed)))
    totalcount = CountRecord(level, "_head", sum([r.total for r in tmp]))

    return CountData([totalcount] + tmp + [CountRecord(level, "_end", 0)])


