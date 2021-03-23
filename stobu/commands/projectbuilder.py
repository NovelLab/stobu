"""Building module for storybuilder project."""


# Official Libraries
import argparse
import os


# My Modules
from stobu.core.basedatabuilder import on_build_basedata
from stobu.core.novelbuilder import on_build_novel
from stobu.core.outlinebuilder import on_build_outline
from stobu.core.plotbuilder import on_build_plot
from stobu.core.sceneinfobuilder import on_build_scene_info
from stobu.core.scriptbuilder import on_build_script
from stobu.core.storydatacreator import get_story_data
from stobu.datatypes import StoryData
from stobu.datatypes import OutputData
from stobu.nametagmanager import get_nametag_db
from stobu.settings import MARKDOWN_EXT
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.dicts import dict_sorted
from stobu.util.fileio import write_file
from stobu.util.filepath import add_extention
from stobu.util.log import logger


__all__ = (
        'switch_command_to_build',
        )


# Define constants
FILENAME_BASEDATA = add_extention('data', MARKDOWN_EXT)
"""str: file name of base data."""

FILENAME_OUTLINE = add_extention('outline', MARKDOWN_EXT)
"""str: file name of outline."""

FILENAME_PLOT = add_extention('plot', MARKDOWN_EXT)
"""str: file name of plot."""

FILENAME_SCRIPT = add_extention('script', MARKDOWN_EXT)
"""str: file name of script."""

FILENAME_NOVEL = add_extention('novel', MARKDOWN_EXT)
"""str: file name of novel."""

FILENAME_SCENE_INFO = add_extention('scene', MARKDOWN_EXT)
"""str: file name of scene info."""


# Main Functions
def switch_command_to_build(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('b', 'build')
    logger.debug("Starting command 'Build'...")

    # create tag db
    tagdb = assertion.is_dict(dict_sorted(get_nametag_db(), True))

    # get story data
    story_data = assertion.is_instance(get_story_data(cmdargs.part), StoryData)

    # - outline
    if cmdargs.outline:
        logger.debug("Building outline data...")
        outline_data = assertion.is_instance(on_build_outline(story_data, tagdb),
                OutputData)
        if outline_data:
            path = os.path.join(ppath.get_build_dir_path(), FILENAME_OUTLINE)
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
            path = os.path.join(ppath.get_build_dir_path(), FILENAME_PLOT)
            if not write_file(path, plot_data.get_serialized_data()):
                logger.error("...Failed to write the output plot data!")
                return False
            else:
                logger.debug("...Succeeded to output the plot data.")
        else:
            logger.error("...Failed to build the output data in plot process!: %s", plot_data)
            return False

    # - scene info
    if cmdargs.info:
        logger.debug("Building scene info...")
        data = assertion.is_instance(
                on_build_scene_info(story_data, tagdb),
                OutputData)
        if data:
            path = os.path.join(ppath.get_build_dir_path(), FILENAME_SCENE_INFO)
            if not write_file(path, data.get_serialized_data()):
                logger.error("...Failed to write the output scene info data!")
                return False
            else:
                logger.debug("...Succeeded to output the scene info data.")
        else:
            logger.error("...Failed to build the output data in scene info process!: %s", data)
            return False

    # - script
    if cmdargs.script:
        logger.debug("Building script data...")
        script_data = assertion.is_instance(
                on_build_script(story_data, tagdb, cmdargs.rubi),
                OutputData)
        if script_data:
            path = os.path.join(ppath.get_build_dir_path(), FILENAME_SCRIPT)
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
        novel_data = assertion.is_instance(
                on_build_novel(story_data, tagdb, cmdargs.rubi),
                OutputData)
        if novel_data:
            path = os.path.join(ppath.get_build_dir_path(), FILENAME_NOVEL)
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
        path = os.path.join(ppath.get_build_dir_path(), FILENAME_BASEDATA)
        if not write_file(path, base_data.get_serialized_data()):
            logger.error("...Failed to write the output base data!")
            return False
        else:
            logger.debug("...Succeeded to output the base data.")
    else:
        logger.error("...Failed to build the output data in base data process!: %s", base_data)
        return False

    return True
