"""Check module for storybuilder project files."""


# Official Libraries
import glob
import os


# My Modules
from storybuilder.settings import PROJECT_FILENAME, BOOK_FILENAME, ORDER_FILENAME
from storybuilder.settings import CHAPTER_DIR, EPISODE_DIR, SCENE_DIR, NOTE_DIR
from storybuilder.settings import PERSON_DIR, STAGE_DIR, ITEM_DIR, WORD_DIR
from storybuilder.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT
from storybuilder.settings import PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
import storybuilder.projectpathmanager as ppath


__all__ = (
        'exists_any_chapter', 'exists_any_episode', 'exists_any_scene', 'exists_any_note',
        'exists_any_person', 'exists_any_stage', 'exists_any_item', 'exists_any_word',
        )


# API Functions
def exists_any_chapter() -> bool:
    """Check if any chapter file exists."""
    return _exists_any_file(ppath.get_chapter_dir_path(), CHAPTER_EXT)


def exists_any_episode() -> bool:
    """Check if any episode file exists."""
    return _exists_any_file(ppath.get_episode_dir_path(), EPISODE_EXT)


def exists_any_item() -> bool:
    """Check if any item file exists."""
    return _exists_any_file(ppath.get_item_dir_path(), ITEM_EXT)


def exists_any_note() -> bool:
    """Check if any note file exists."""
    return _exists_any_file(ppath.get_note_dir_path(), NOTE_EXT)


def exists_any_person() -> bool:
    """Check if any person file exists."""
    return _exists_any_file(ppath.get_person_dir_path(), PERSON_EXT)


def exists_any_scene() -> bool:
    """Check if any scene file exists."""
    return _exists_any_file(ppath.get_scene_dir_path(), SCENE_EXT)


def exists_any_stage() -> bool:
    """Check if any stage file exists."""
    return _exists_any_file(ppath.get_stage_dir_path(), STAGE_EXT)


def exists_any_word() -> bool:
    """Check if any word file exists."""
    return _exists_any_file(ppath.get_word_dir_path(), WORD_EXT)


def exists_book_file() -> bool:
    """Check if book file exists."""
    return _is_exists_file(ppath.get_book_path())


def exists_order_file() -> bool:
    """Check if order file exists."""
    return _is_exists_file(ppath.get_order_path())


def exists_project_file() -> bool:
    """Check if project file exists."""
    return _is_exists_file(ppath.get_project_path())


def is_exists_the_chapter(fname: str) -> bool:
    """Check if the chapter file exists."""
    return _is_exists_file(ppath.get_chapter_path(fname))


def is_exists_the_episode(fname: str) -> bool:
    """Check if the episode file exists."""
    return _is_exists_file(ppath.get_episode_path(fname))


def is_exists_the_item(fname: str) -> bool:
    """Check if the item file exists."""
    return _is_exists_file(ppath.get_item_path(fname))


def is_exists_the_note(fname: str) -> bool:
    """Check if the note file exists."""
    return _is_exists_file(ppath.get_note_path(fname))


def is_exists_the_person(fname: str) -> bool:
    """Check if the person file exists."""
    return _is_exists_file(ppath.get_person_path(fname))


def is_exists_the_scene(fname: str) -> bool:
    """Check if the scene file exists."""
    return _is_exists_file(ppath.get_scene_path(fname))


def is_exists_the_stage(fname: str) -> bool:
    """Check if the stage file exists."""
    return _is_exists_file(ppath.get_stage_path(fname))


def is_exists_the_word(fname: str) -> bool:
    """Check if the word file exists."""
    return _is_exists_file(ppath.get_word_path(fname))


# Private Functions
def _exists_any_file(dirname: str, ext: str) -> bool:
    return len(glob.glob(os.path.join(dirname, f"*.{ext}"))) > 0


def _is_exists_file(filepath: str) -> bool:
    return os.path.exists(filepath)

