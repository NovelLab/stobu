"""Template create module."""

# Official Libraries
import os


# My Modules
from stobu.paths.projects import MARKDOWN_EXT, YAML_EXT
from stobu.syss.settings import VERSION, DEFAULT_EDITOR
from stobu.syss import messages as msg
from stobu.tools.pathchecker import is_duplicated_path_in_dir
from stobu.tools.pathgetter import get_app_path, add_extention
from stobu.tools.pathgetter import filepath_of
from stobu.types.element import ElmType
from stobu.utils.fileio import read_file
from stobu.utils.log import logger


__all__ = (
        'get_template_data',
        )


# Define Constants
PROC = 'TEMPLATE CREATOR'


DATA_DIR = 'data'


TEMP_FILES = {
        ElmType.BOOK: 'book_tmp',
        ElmType.BUILD: '',
        ElmType.CHAPTER: 'chapter_tmp',
        ElmType.EPISODE: 'episode_tmp',
        ElmType.EVENT: 'event_tmp',
        ElmType.ITEM: 'item_tmp',
        ElmType.MATERIAL: '',
        ElmType.MOB: 'mob_tmp',
        ElmType.NONE: '',
        ElmType.NOTE: 'note_tmp',
        ElmType.ORDER: 'order_tmp',
        ElmType.OUTLINE: 'outline_tmp',
        ElmType.PERSON: 'person_tmp',
        ElmType.PLAN: 'plan_tmp',
        ElmType.PLOT: 'plot_tmp',
        ElmType.PROJECT: 'project_tmp',
        ElmType.RUBI: 'rubi_tmp',
        ElmType.SCENE: 'scene_tmp',
        ElmType.STAGE: 'stage_tmp',
        ElmType.TIME: 'time_tmp',
        ElmType.TODO: 'todo_tmp',
        ElmType.WORD: 'word_tmp',
        }


TEMP_EXTS = {
        ElmType.BOOK: YAML_EXT,
        ElmType.BUILD: MARKDOWN_EXT,
        ElmType.CHAPTER: MARKDOWN_EXT,
        ElmType.EPISODE: MARKDOWN_EXT,
        ElmType.EVENT: MARKDOWN_EXT,
        ElmType.ITEM: MARKDOWN_EXT,
        ElmType.MATERIAL: MARKDOWN_EXT,
        ElmType.MOB: YAML_EXT,
        ElmType.NONE: MARKDOWN_EXT,
        ElmType.NOTE: MARKDOWN_EXT,
        ElmType.ORDER: YAML_EXT,
        ElmType.OUTLINE: MARKDOWN_EXT,
        ElmType.PERSON: MARKDOWN_EXT,
        ElmType.PLAN: MARKDOWN_EXT,
        ElmType.PLOT: YAML_EXT,
        ElmType.PROJECT: YAML_EXT,
        ElmType.RUBI: YAML_EXT,
        ElmType.SCENE: MARKDOWN_EXT,
        ElmType.STAGE: MARKDOWN_EXT,
        ElmType.TIME: YAML_EXT,
        ElmType.TODO: MARKDOWN_EXT,
        ElmType.TRASH: MARKDOWN_EXT,
        ElmType.WORD: MARKDOWN_EXT,
        }


WITH_PLOT = [
        ElmType.BOOK,
        ElmType.CHAPTER,
        ElmType.EPISODE,
        ElmType.SCENE,
        ]


# Main
def get_template_data(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    path = _get_filename(elm)
    data = read_file(path)

    if elm in WITH_PLOT:
        plot = read_file(_get_filename(ElmType.PLOT))
        return data.replace('{PLOT}', plot)
    elif ElmType.PROJECT is elm:
        return data.replace('{VERSION}', VERSION).replace('{EDITOR}', DEFAULT_EDITOR)
    else:
        return data


# Private Functions
def _get_filename(elm: ElmType) -> str:
    assert isinstance(elm, ElmType)

    dirpath = os.path.join(get_app_path(), DATA_DIR)

    return os.path.join(dirpath, add_extention(TEMP_FILES[elm], TEMP_EXTS[elm]))
