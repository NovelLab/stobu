"""Build project module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.core.actiondatacreator import actions_data_from
from stobu.core.baseinfocreator import base_info_outputs_data_from
from stobu.core.contentsdatacreator import contents_data_from, outputs_data_from_contents_data
from stobu.core.nametagcreator import get_nametags
from stobu.core.noveler import novels_data_from, outputs_data_from_novels_data
from stobu.core.outliner import outlines_data_from, outputs_data_from_outlines_data
from stobu.core.plotter import plots_data_from, outputs_data_from_plots_data
from stobu.core.scripter import outputs_data_from_scripts_data, scripts_data_from
from stobu.core.storydatacreator import story_data_from
from stobu.syss import messages as msg
from stobu.tools.buildchecker import has_build_of
from stobu.tools.cmdchecker import has_cmd_of
from stobu.tools.pathgetter import filepath_of
from stobu.types.build import BuildType
from stobu.types.content import ContentsData
from stobu.types.command import CmdType
from stobu.types.element import ElmType
from stobu.types.output import OutputsData
from stobu.types.story import StoryData
from stobu.utils import assertion
from stobu.utils.fileio import write_file
from stobu.utils.log import logger


__all__ = (
        'build_project',
        )


# Define Constants
PROC = 'COMMAND BUILD'


BUILD_FILENAMES = {
        BuildType.NONE: 'none',
        BuildType.BASE: 'basedata',
        BuildType.NOVEL: 'novel',
        BuildType.OUTLINE: 'outline',
        BuildType.PLOT: 'plot',
        BuildType.SCRIPT: 'script',
        }


# Main
def build_project(args: Namespace) -> bool:
    assert isinstance(args, Namespace)
    assert has_cmd_of(args, CmdType.BUILD)

    tags = assertion.is_dict(get_nametags())
    if not tags:
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"name tags in {PROC}"))
        return False

    story_data = story_data_from(args)
    if not story_data or not isinstance(story_data, StoryData) or not story_data.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"story data in {PROC}"))
        return False

    contents_data = contents_data_from(story_data, tags)
    if not contents_data or not isinstance(contents_data, ContentsData) or not contents_data.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"contents datain {PROC}"))
        return False

    output_contents_data = outputs_data_from_contents_data(contents_data)
    if not output_contents_data or not isinstance(output_contents_data, OutputsData) or not output_contents_data.has_data():
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"output contents data in {PROC}"))
        return False

    if has_build_of(args, BuildType.OUTLINE):
        logger.debug(msg.PROC_START.format(proc=f"build outline in {PROC}"))

        outlines = outlines_data_from(story_data, tags)
        if not outlines or not outlines.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"outlines data in {PROC}"))
            return False

        outputs = output_contents_data.cloned() + outputs_data_from_outlines_data(outlines, tags)
        if not _output_data(BuildType.OUTLINE, outputs):
            logger.error(msg.PROC_FAILED.format(proc=f"outline in {PROC}"))
            return False

    if has_build_of(args, BuildType.PLOT):
        logger.debug(msg.PROC_START.format(proc=f"build plot in {PROC}"))

        plots = plots_data_from(story_data)
        if not plots or not plots.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"plots data in {PROC}"))
            return False

        outputs = output_contents_data.cloned() + outputs_data_from_plots_data(plots, tags)
        if not _output_data(BuildType.PLOT, outputs):
            logger.error(msg.PROC_FAILED.format(proc=f"plot in {PROC}"))
            return False

    actions_data = actions_data_from(story_data)
    if not actions_data or not actions_data.has_data():
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"actions data in {PROC}"))

    if has_build_of(args, BuildType.SCRIPT):
        logger.debug(msg.PROC_START.format(proc=f"build script in {PROC}"))
        scripts = scripts_data_from(actions_data, tags)
        if not scripts or not scripts.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"scripts data in {PROC}"))
            return False

        outputs = output_contents_data.cloned() + outputs_data_from_scripts_data(scripts, tags)
        if not _output_data(BuildType.SCRIPT, outputs):
            logger.error(msg.PROC_FAILED.format(proc=f"script in {PROC}"))
            return False

    if has_build_of(args, BuildType.NOVEL):
        logger.debug(msg.PROC_START.format(proc=f"build novel in {PROC}"))
        novels = novels_data_from(actions_data, tags)
        if not novels or not novels.has_data():
            logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"novels data in {PROC}"))
            return False

        outputs = output_contents_data.cloned() + outputs_data_from_novels_data(novels, tags)
        if not _output_data(BuildType.NOVEL, outputs):
            logger.error(msg.PROC_FAILED.format(proc=f"novel in {PROC}"))
            return False

    # base data
    base_data = base_info_outputs_data_from(args, story_data, actions_data, tags)
    if not base_data or not base_data.has_data():
        logger.error(msg.PROC_FAILED.format(proc=f"base data in {PROC}"))
        return False

    if not _output_data(BuildType.BASE, base_data):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(data=f"base data in {PROC}"))
        return False

    # detail data

    return True


# Private Functions
def _output_data(build_type: BuildType, outputs_data: OutputsData) -> bool:
    assert isinstance(build_type, BuildType)
    assert isinstance(outputs_data, OutputsData)
    logger.debug(msg.PROC_START.format(proc=f"output {build_type} in {PROC}"))

    path = filepath_of(ElmType.BUILD, BUILD_FILENAMES[build_type])
    if not write_file(path, outputs_data.get_serialized_data()):
        logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"outputs data {str(build_type)} in {PROC}"))
        return False

    logger.debug(msg.PROC_SUCCESS.format(proc=f"output {build_type} in {PROC}"))
    return True
