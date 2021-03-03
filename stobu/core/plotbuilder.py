"""Build plot data module for storybuilder project."""


# Official Libraries


# My Modules
from stobu.core.contentscreator import get_contents_list
from stobu.dataconverter import conv_text_list_by_tags
from stobu.datatypes import ContentsData
from stobu.datatypes import OutputData
from stobu.datatypes import PlotData, PlotRecord
from stobu.datatypes import StoryData, StoryRecord
from stobu.formatter import format_contents_table_data, format_plot_data, get_breakline
from stobu.util import assertion
from stobu.util.log import logger


__all__ = (
        'on_build_plot',
        'get_plot_data',
        )


# Main Function
def on_build_plot(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    contents = assertion.is_instance(get_contents_list(story_data), ContentsData)
    books = assertion.is_instance(get_plot_data('book', story_data), PlotData)
    chapters = assertion.is_instance(get_plot_data('chapter', story_data), PlotData)
    episodes = assertion.is_instance(get_plot_data('episode', story_data), PlotData)
    scenes = assertion.is_instance(get_plot_data('scene', story_data), PlotData)

    plots = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_plot_data('book', books) \
            + [get_breakline()] \
            + format_plot_data('chapter', chapters) \
            + [get_breakline()] \
            + format_plot_data('episode', episodes) \
            + [get_breakline()] \
            + format_plot_data('scene', scenes)

    output_data = conv_text_list_by_tags(plots, tags)

    return OutputData(output_data)


# Functions
def get_plot_data(level: str, story_data: StoryData) -> PlotData:
    assert isinstance(level, str)
    assert isinstance(story_data, StoryData)

    tmp = []

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if level == record.category:
            plot = record.data['plot']
            tmp.append(
                    PlotRecord(record.data['title'],
                        plot['setup'],
                        plot['tp1st'],
                        plot['develop'],
                        plot['tp2nd'],
                        plot['climax'],
                        plot['resolve']))
        else:
            continue

    return PlotData(tmp)

