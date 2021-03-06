"""Initialize module for storybuilder's project."""


# Official Libraries
import os


# My Modules
from stobu.settings import PROJECT_FILENAME, BOOK_FILENAME, ORDER_FILENAME, RUBI_FILENAME
from stobu.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT, PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.settings import BUILD_DIR, CHAPTER_DIR, EPISODE_DIR, SCENE_DIR, NOTE_DIR, PERSON_DIR, STAGE_DIR, ITEM_DIR, WORD_DIR, TRASH_DIR
from stobu.templatecreator import TemplateCreator
from stobu.tools import filechecker as checker
from stobu.util.fileio import write_file
from stobu.util.filepath import get_current_path, is_exists_path
from stobu.util.log import logger


# Main Function
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

    if not check_and_create_chapter_dir() \
            or not check_and_create_episode_dir() \
            or not check_and_create_scene_dir() \
            or not check_and_create_note_dir() \
            or not check_and_create_person_dir() \
            or not check_and_create_stage_dir() \
            or not check_and_create_item_dir() \
            or not check_and_create_word_dir() \
            or not check_and_create_trash_dir() \
            or not check_and_create_build_dir():
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
            or not check_and_create_a_chapter_file(creator) \
            or not check_and_create_a_episode_file(creator) \
            or not check_and_create_a_scene_file(creator) \
            or not check_and_create_a_note_file(creator) \
            or not check_and_create_a_person_file(creator) \
            or not check_and_create_a_stage_file(creator) \
            or not check_and_create_a_item_file(creator) \
            or not check_and_create_a_word_file(creator):
        logger.error("Failed check and create default files!")
        return False

    logger.debug("...Succeeded the check and create default files.")
    return True


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


def check_and_create_build_dir() -> bool:
    logger.debug("Checking and Creating build directory...")

    path = os.path.join(get_current_path(), BUILD_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create build directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create build directory.")
    return True


def check_and_create_chapter_dir() -> bool:
    logger.debug("Checking and Creating chapter directory...")

    path = os.path.join(get_current_path(), CHAPTER_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create chapter directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create chapter directory.")
    return True


def check_and_create_episode_dir() -> bool:
    logger.debug("Checking and Creating episode directory...")

    path = os.path.join(get_current_path(), EPISODE_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create episode directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create episode directory.")
    return True


def check_and_create_item_dir() -> bool:
    logger.debug("Checking and Creating item directory...")

    path = os.path.join(get_current_path(), ITEM_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create item directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create item directory.")
    return True


def check_and_create_note_dir() -> bool:
    logger.debug("Checking and Creating note directory...")

    path = os.path.join(get_current_path(), NOTE_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create note directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create note directory.")
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


def check_and_create_person_dir() -> bool:
    logger.debug("Checking and Creating person directory...")

    path = os.path.join(get_current_path(), PERSON_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create the directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create person dir.")
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


def check_and_create_scene_dir() -> bool:
    logger.debug("Checking and Creating scene directory...")

    path = os.path.join(get_current_path(), SCENE_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create the directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create scene dir.")
    return True


def check_and_create_stage_dir() -> bool:
    logger.debug("Checking and Creating stage directory...")

    path = os.path.join(get_current_path(), STAGE_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create the directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create stage dir.")
    return True


def check_and_create_trash_dir() -> bool:
    logger.debug("Checking and Creating trash directory...")

    path = os.path.join(get_current_path(), TRASH_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create the directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create trash dir.")
    return True


def check_and_create_word_dir() -> bool:
    logger.debug("Checking and Creating word directory...")

    path = os.path.join(get_current_path(), WORD_DIR)
    if not safe_create_directory(path):
        logger.error("Failed check or create the directory!: %s", path)
        return False

    logger.debug("...Succeeded check and create word dir.")
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

    return True
