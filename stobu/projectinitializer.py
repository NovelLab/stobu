"""Initialize module for storybuilder's project."""


# Official Libraries
import os


# My Modules
from stobu.settings import PROJECT_FILENAME, BOOK_FILENAME, ORDER_FILENAME, RUBI_FILENAME
from stobu.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT, PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.settings import BUILD_DIR, CHAPTER_DIR, EPISODE_DIR, SCENE_DIR, NOTE_DIR, PERSON_DIR, STAGE_DIR, ITEM_DIR, WORD_DIR, TRASH_DIR
from stobu.settings import PLAN_DIR, OUTLINE_DIR, MATERIAL_DIR
from stobu.templatecreator import TemplateCreator
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util.fileio import write_file
from stobu.util.filepath import get_current_path, is_exists_path
from stobu.util.log import logger


__all__ = (
        )


# Define Constants
START_PROCESS_CHECK_AND_CREATE = 'Starting the check and create {target}...'
"""str: message template for start process to check and create any."""

FINISH_PROCESS_CHECK_AND_CREATE = '...Succeeded the check and create {target}.'
"""str: message template for finish process to check and create any."""

ERR_CHECK_AND_CREATE = '...Failed the check or create {target}!: %s'
"""str: error message template for check or create any."""


# Main Function
def init_project() -> bool:
    logger.debug("Starting Project Initializer...")

    creator = TemplateCreator.get_instance()
    if not creator:
        logger.error("Missing TemplateCreator. not initialized!: %s", creator)
        return False

    if has_project_file():
        logger.debug("Already Initialized this project!")
    else:
        if not create_project_file(creator):
            logger.debug("Failure creating the project file!")
            return False

    if not check_and_create_defaults(creator):
        logger.error("Failed check and create defaults!")
        return False

    logger.debug("...Succeeded init project.")
    return True


def check_and_create_defaults(creator: TemplateCreator) -> bool:
    logger.debug("Starting the check and create default dir and files...")
    assert isinstance(creator, TemplateCreator)

    if not check_and_create_default_dirs():
        logger.error("Failed the check and create default directories!")
        return False

    if not check_and_create_default_files(creator):
        logger.error("Failed the check and create default files!")
        return False

    logger.debug("...Succeeded the check and create defaults.")
    return True


def check_and_create_default_dirs() -> bool:
    logger.debug("Starting the check and create default directories...")

    if not _check_and_create_dir('chapter', CHAPTER_DIR) \
            or not _check_and_create_dir('episode', EPISODE_DIR) \
            or not _check_and_create_dir('scene', SCENE_DIR) \
            or not _check_and_create_dir('note', NOTE_DIR) \
            or not _check_and_create_dir('person', PERSON_DIR) \
            or not _check_and_create_dir('stage', STAGE_DIR) \
            or not _check_and_create_dir('item', ITEM_DIR) \
            or not _check_and_create_dir('word', WORD_DIR) \
            or not _check_and_create_dir('trash', TRASH_DIR) \
            or not _check_and_create_dir('material', MATERIAL_DIR) \
            or not _check_and_create_dir('plan', PLAN_DIR) \
            or not _check_and_create_dir('outline', OUTLINE_DIR) \
            or not _check_and_create_dir('build', BUILD_DIR):
        logger.error("Failed check and create default dirs!")
        return False

    logger.debug("...Succeeded check and create default directories.")
    return True


def check_and_create_default_files(creator: TemplateCreator) -> bool:
    logger.debug("Starting the check and create default files...")
    assert isinstance(creator, TemplateCreator)

    if not check_and_create_book_file(creator) \
            or not check_and_create_order_file(creator) \
            or not check_and_create_rubi_file(creator) \
            or not check_and_create_todo_file(creator) \
            or not check_and_create_a_chapter_file(creator) \
            or not check_and_create_a_episode_file(creator) \
            or not check_and_create_a_scene_file(creator) \
            or not check_and_create_a_note_file(creator) \
            or not check_and_create_a_plan_file(creator) \
            or not check_and_create_a_outline_file(creator) \
            or not check_and_create_a_person_file(creator) \
            or not check_and_create_a_stage_file(creator) \
            or not check_and_create_a_item_file(creator) \
            or not check_and_create_a_word_file(creator):
        logger.error("Failed check and create default files!")
        return False

    logger.debug("...Succeeded the check and create default files.")
    return True


# Functions
def check_and_create_a_chapter_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a chapter file...")

    if checker.exists_any_chapter():
        logger.debug("Already exists any chapter file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), CHAPTER_DIR), f"main.{CHAPTER_EXT}")
    template_data = creator.get_chapter_template()
    if not template_data:
        logger.error("Missing the chapter template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the chapter template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a chapter file.")
    return True


def check_and_create_a_episode_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a episode file...")

    if checker.exists_any_episode():
        logger.debug("Already exists any episode file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), EPISODE_DIR), f"main.{EPISODE_EXT}")
    template_data = creator.get_episode_template()
    if not template_data:
        logger.error("Missing the episode template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the episode template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a episode file.")
    return True


def check_and_create_a_item_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a item file...")

    if checker.exists_any_item():
        logger.debug("Already exists any item file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), ITEM_DIR), f"main.{ITEM_EXT}")
    template_data = creator.get_item_template()
    if not template_data:
        logger.error("Missing the item template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the item template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a item file.")
    return True


def check_and_create_a_note_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a note file...")

    if checker.exists_any_note():
        logger.debug("Already exists any note file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), NOTE_DIR), f"main.{NOTE_EXT}")
    template_data = creator.get_note_template()
    if not template_data:
        logger.error("Missing the note template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the note template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a note file.")
    return True


def check_and_create_a_outline_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a outline file...")

    if checker.exists_any_outline():
        logger.debug("Already exists any outline file. Succeeded.")
        return True

    template_data = creator.get_outline_template()
    if not template_data:
        logger.error("Missing the outline template data!: %s", template_data)
        return False

    if not write_file(ppath.get_outline_path('main'), template_data):
        logger.error("Failed write the outline template data!: %s", 'main')
        return False

    logger.debug("...Succeeded check and create a outline file.")
    return True


def check_and_create_a_person_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a person file...")

    if checker.exists_any_person():
        logger.debug("Already exists any person file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), PERSON_DIR), f"main.{PERSON_EXT}")
    template_data = creator.get_person_template()
    if not template_data:
        logger.error("Missing the person template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the person template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a person file.")
    return True


def check_and_create_a_plan_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a plan file...")

    if checker.exists_any_plan():
        logger.debug("Already exists any plan file. Succeeded.")
        return True

    template_data = creator.get_plan_template()
    if not template_data:
        logger.error("Missing the plan template data!: %s", template_data)
        return False

    if not write_file(ppath.get_plan_path('main'), template_data):
        logger.error("Failed write the plan template data!: %s", 'main')
        return False

    logger.debug("...Succeeded check and create a plan file.")
    return True



def check_and_create_a_scene_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a scene file...")

    if checker.exists_any_scene():
        logger.debug("Already exists any scene file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), SCENE_DIR), f"main.{SCENE_EXT}")
    template_data = creator.get_scene_template()
    if not template_data:
        logger.error("Missing the scene template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the scene template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a scene file.")
    return True


def check_and_create_a_stage_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a stage file...")

    if checker.exists_any_stage():
        logger.debug("Already exists any stage file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), STAGE_DIR), f"main.{STAGE_EXT}")
    template_data = creator.get_stage_template()
    if not template_data:
        logger.error("Missing the stage template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the stage template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a stage file.")
    return True


def check_and_create_a_word_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a word file...")

    if checker.exists_any_word():
        logger.debug("Already exists any word file. Succeeded.")
        return True

    path = os.path.join(
            os.path.join(get_current_path(), WORD_DIR), f"main.{WORD_EXT}")
    template_data = creator.get_word_template()
    if not template_data:
        logger.error("Missing the word template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the word template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create a word file.")
    return True


def check_and_create_book_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating the book file...")

    if has_book_file():
        logger.debug("Already the book file exists. Succeeded.")
        return True

    path = os.path.join(get_current_path(), BOOK_FILENAME)
    template_data = creator.get_book_template()
    if not template_data:
        logger.error("Missing the book template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the book template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create the book file.")
    return True


def check_and_create_order_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating order file...")

    if has_order_file():
        logger.debug("Already exists the order file!")
        return True

    path = get_order_file_path()
    template_data = creator.get_order_template()
    if not template_data:
        logger.error("Missing the order template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the order template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create order file.")
    return True


def check_and_create_rubi_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating a rubi file...")

    if has_rubi_file():
        logger.debug("Already the rubi file exists. Succeeded.")
        return True

    path = os.path.join(get_current_path(), RUBI_FILENAME)
    template_data = creator.get_rubi_template()
    if not template_data:
        logger.error("Missing the rubi template data!: %s", template_data)
        return False

    if not write_file(path, template_data):
        logger.error("Failed write the rubi template data!: %s", path)
        return False

    logger.debug("...Succeeded check and create the rubi file.")
    return True


def check_and_create_todo_file(creator: TemplateCreator) -> bool:
    logger.debug("Checking and Creating todo file...")

    if checker.exists_todo_file():
        logger.debug("Already exists the todo file!")
        return True

    template_data = creator.get_todo_template()
    if not template_data:
        logger.error("Missing the todo template data!: %s", template_data)
        return False

    if not write_file(ppath.get_todo_path(), template_data):
        logger.error("Failed write the todo template data!")
        return False

    logger.debug("...Succeeded check and create todo file.")
    return True


def create_project_file(creator: TemplateCreator) -> bool:
    logger.debug("Creating the project file...")
    assert isinstance(creator, TemplateCreator)

    template_data = creator.get_project_template()
    if not template_data:
        logger.error("Missing a project template data!: %s", template_data)
        return False

    if not write_file(get_project_file_path(), template_data):
        logger.error("Failed create project file!")
        return False

    logger.debug("...Succeeded create project file.")
    return True


def get_book_file_path() -> str:
    """Get the book file path."""
    return os.path.join(get_current_path(), BOOK_FILENAME)


def get_order_file_path() -> str:
    """Get the order file path."""
    return os.path.join(get_current_path(), ORDER_FILENAME)


def get_project_file_path() -> str:
    """Get a project file path."""
    return os.path.join(get_current_path(), PROJECT_FILENAME)


def get_rubi_file_path() -> str:
    """Get a rubi file path."""
    return os.path.join(get_current_path(), RUBI_FILENAME)


def get_todo_file_path() -> str:
    return ppath.get_todo_path()


def has_book_file() -> bool:
    """Check if a book file exists."""
    return is_exists_path(get_book_file_path())


def has_order_file() -> bool:
    """Check if a order file exists."""
    return is_exists_path(get_order_file_path())


def has_project_file() -> bool:
    """Check if a project file exists."""
    return is_exists_path(get_project_file_path())


def has_rubi_file() -> bool:
    """Check if a rubi file exists."""
    return is_exists_path(get_rubi_file_path())


def safe_create_directory(dirname: str) -> bool:
    """Check and create a directory."""

    if not is_exists_path(dirname):
        os.makedirs(dirname)
    else:
        logger.debug("> Already exists the directory: %s", dirname)

    return True


# Private Functions
def _check_and_create_dir(target: str, dir_name: str) -> bool:
    assert isinstance(target, str)
    assert isinstance(dir_name, str)

    _target = f"{target} directory"
    logger.debug(START_PROCESS_CHECK_AND_CREATE.format(target=_target))

    path = os.path.join(get_current_path(), dir_name)
    if not safe_create_directory(path):
        logger.error(ERR_CHECK_AND_CREATE.format(target=_target), path)
        return False

    logger.debug(FINISH_PROCESS_CHECK_AND_CREATE.format(target=_target))
    return True

