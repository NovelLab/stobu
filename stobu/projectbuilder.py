"""Building module for storybuilder project."""


# Official Libraries
import argparse
import os


# My Modules
from stobu.core.basedatabuilder import on_build_basedata
from stobu.core.novelbuilder import on_build_novel
from stobu.core.outlinebuilder import on_build_outline
from stobu.core.plotbuilder import on_build_plot
from stobu.core.scriptbuilder import on_build_script
from stobu.core.storydatacreator import get_story_data
from stobu.datatypes import StoryData
from stobu.datatypes import OutputData
from stobu.nametagmanager import get_nametag_db
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import write_file
from stobu.util.log import logger


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
    story_data = assertion.is_instance(get_story_data(cmdargs.part), StoryData)

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
        script_data = assertion.is_instance(
                on_build_script(story_data, tagdb, cmdargs.rubi),
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
        novel_data = assertion.is_instance(
                on_build_novel(story_data, tagdb, cmdargs.rubi),
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
