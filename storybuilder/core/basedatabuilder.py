"""Builb base data of storybuilder project."""


# Official Libraries
import argparse


# My Modules
from storybuilder.core.charcounter import on_build_novel_charcounts, on_build_outline_charcounts, on_build_plot_charcounts, on_build_script_charcounts
from storybuilder.core.contentscreator import get_contents_list
from storybuilder.dataconverter import conv_text_list_by_tags
from storybuilder.datatypes import OutputData
from storybuilder.datatypes import StoryData
from storybuilder.formatter import format_contents_table_data, get_breakline
from storybuilder.util.log import logger


__all__ = (
        'on_build_basedata',
        )


# Main Function
def on_build_basedata(cmdargs: argparse.Namespace,
        story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(cmdargs, argparse.Namespace)
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    tmp = []

    if cmdargs.outline:
        # outline data
        tmp.extend(on_build_outline_charcounts(story_data, tags).get_data())
        tmp.append('\n')
        tmp.append(get_breakline())
    if cmdargs.plot:
        # plot data
        tmp.extend(on_build_plot_charcounts(story_data, tags).get_data())
        tmp.append('\n')
        tmp.append(get_breakline())
    if cmdargs.script:
        # script data
        tmp.extend(on_build_script_charcounts(story_data, tags).get_data())
        tmp.append('\n')
        tmp.append(get_breakline())
    if cmdargs.novel:
        # novel data
        tmp.extend(on_build_novel_charcounts(story_data, tags).get_data())
        tmp.append('\n')
        tmp.append(get_breakline())

    contents = get_contents_list(story_data)

    basedata = format_contents_table_data(contents) \
            + ['\n', get_breakline()] \
            + tmp

    output_data = conv_text_list_by_tags(basedata, tags)

    return OutputData(output_data)
