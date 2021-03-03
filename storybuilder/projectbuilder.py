"""Building module for storybuilder project."""


# Official Libraries
import argparse
import os


# My Modules
from storybuilder.core.basedatabuilder import on_build_basedata
from storybuilder.core.novelbuilder import on_build_novel
from storybuilder.core.outlinebuilder import on_build_outline
from storybuilder.core.plotbuilder import on_build_plot
from storybuilder.core.scriptbuilder import on_build_script
from storybuilder.core.storydatacreator import get_story_data
from storybuilder.dataconverter import conv_action_record_from_scene_action, conv_text_from_tag, conv_to_story_record, conv_code_from_action_record
from storybuilder.datatypes import StoryRecord, OutlineRecord, ContentRecord, PlotRecord, ActionRecord, StoryCode
from storybuilder.datatypes import CountRecord
from storybuilder.datatypes import StoryData
from storybuilder.datatypes import OutputData
from storybuilder.formatter import format_contents_table_data, format_outline_data, format_plot_data, format_script_data, format_novel_data
from storybuilder.formatter import format_charcounts_outline, format_charcounts_plot, format_charcounts_script, format_charcounts_novel
from storybuilder.formatter import get_breakline
from storybuilder.instructions import apply_instruction_to_action_data
from storybuilder.nametagmanager import NameTagDB, get_nametag_db
from storybuilder.projectcounter import get_charcounts_script_data, get_charcounts_novel_data
import storybuilder.projectpathmanager as ppath
from storybuilder.util import assertion
from storybuilder.util.fileio import read_file_as_yaml, read_file_as_markdown, write_file
from storybuilder.util.filepath import basename_of
from storybuilder.util.log import logger


__all__ = (
        'switch_command_to_build',
        )


# Main Functions
def switch_command_to_build(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('b', 'build')
    logger.debug("Starting command 'Build'...")

    # create tag db
    tagdb = get_nametag_db()

    # get story data
    story_data = assertion.is_instance(get_story_data(), StoryData)

    # - outline
    if cmdargs.outline:
        logger.debug("Building outline data...")
        outline_data = assertion.is_instance(on_build_outline(story_data, tagdb),
                OutputData)
        if outline_data:
            path = os.path.join(ppath.get_build_dir_path(), "outline.md")
            if not write_file(path, outline_data.get_serialized_data()):
                logger.error("...Failed to write the output outline data!")
                return False
            else:
                logger.debug("...Succeeded to output the outline data.")
        else:
            logger.error("...Failed to build the output data in outline process!: %s", outline_data)
            return False

    # - plot
    if cmdargs.plot:
        logger.debug("Building plot data...")
        plot_data = assertion.is_instance(on_build_plot(story_data, tagdb),
                OutputData)
        if plot_data:
            path = os.path.join(ppath.get_build_dir_path(), "plot.md")
            if not write_file(path, plot_data.get_serialized_data()):
                logger.error("...Failed to write the output plot data!")
                return False
            else:
                logger.debug("...Succeeded to output the plot data.")
        else:
            logger.error("...Failed to build the output data in plot process!: %s", plot_data)
            return False

    # - script
    if cmdargs.script:
        logger.debug("Building script data...")
        script_data = assertion.is_instance(on_build_script(story_data, tagdb),
                OutputData)
        if script_data:
            path = os.path.join(ppath.get_build_dir_path(), "script.md")
            if not write_file(path, script_data.get_serialized_data()):
                logger.error("...Failed to write the output script data!")
                return False
            else:
                logger.debug("...Succeeded to output the script data.")
        else:
            logger.error("...Failed to build the output data in script process!: %s", script_data)
            return False

    # - novel
    if cmdargs.novel:
        logger.debug("Building novel data...")
        novel_data = assertion.is_instance(on_build_novel(story_data, tagdb),
                OutputData)
        if novel_data:
            path = os.path.join(ppath.get_build_dir_path(), "novel.md")
            if not write_file(path, novel_data.get_serialized_data()):
                logger.error("...Failed to write the output novel data!")
                return False
            else:
                logger.debug("...Succeeded to output the novel data.")
        else:
            logger.error("...Failed to build the output data in novel process!: %s", novel_data)
            return False

    # - base data
    base_data = assertion.is_instance(on_build_basedata(cmdargs, story_data, tagdb),
            OutputData)
    if base_data:
        path = os.path.join(ppath.get_build_dir_path(), "data.md")
        if not write_file(path, base_data.get_serialized_data()):
            logger.error("...Failed to write the output base data!")
            return False
        else:
            logger.debug("...Succeeded to output the base data.")
    else:
        logger.error("...Failed to build the output data in base data process!: %s", base_data)
        return False

    return True

