"""Check module for storybuilder project files."""


# Official Libraries
import glob
import os


# My Modules
from stobu.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT
from stobu.settings import PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.settings import PLAN_EXT, OUTLINE_EXT, EVENT_EXT
from stobu.tools import pathmanager as ppath


__all__ = (
        'exists_any_chapter', 'exists_any_episode', 'exists_any_scene', 'exists_any_note',
        'exists_any_person', 'exists_any_stage', 'exists_any_item', 'exists_any_word',
        'exists_any_plan', 'exists_any_outline', 'exists_any_event',
        'exists_project_file',
        'exists_book_file',
        'exists_order_file',
        'exists_rubi_file',
        'exists_todo_file',
        'is_invalid_filename',
        'is_exists_the_chapter', 'is_exists_the_episode', 'is_exists_the_scene', 'is_exists_the_note',
        'is_exists_the_person', 'is_exists_the_stage', 'is_exists_the_item', 'is_exists_the_word',
        'is_exists_the_plan', 'is_exists_the_outline', 'is_exists_the_event',
        )


# API Functions
def exists_any_chapter() -> bool:
    """Check if any chapter file exists."""
    return _exists_any_file(ppath.get_chapter_dir_path(), CHAPTER_EXT)


def exists_any_episode() -> bool:
    """Check if any episode file exists."""
    return _exists_any_file(ppath.get_episode_dir_path(), EPISODE_EXT)


def exists_any_event() -> bool:
    """Check if any event file exists."""
    return _exists_any_file(ppath.get_event_dir_path(), EVENT_EXT)


def exists_any_item() -> bool:
    """Check if any item file exists."""
    return _exists_any_file(ppath.get_item_dir_path(), ITEM_EXT)


def exists_any_note() -> bool:
    """Check if any note file exists."""
    return _exists_any_file(ppath.get_note_dir_path(), NOTE_EXT)


def exists_any_outline() -> bool:
    """Check if any outline file exists."""
    return _exists_any_file(ppath.get_outline_dir_path(), OUTLINE_EXT)


def exists_any_person() -> bool:
    """Check if any person file exists."""
    return _exists_any_file(ppath.get_person_dir_path(), PERSON_EXT)


def exists_any_plan() -> bool:
    """Check if any plan file exists."""
    return _exists_any_file(ppath.get_plan_dir_path(), PLAN_EXT)


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


def exists_rubi_file() -> bool:
    """Check if rubi file exists."""
    return _is_exists_file(ppath.get_rubi_path())


def exists_todo_file() -> bool:
    """Check if todo file exists."""
    return _is_exists_file(ppath.get_todo_path())


def is_exists_the_chapter(fname: str) -> bool:
    """Check if the chapter file exists."""
    return _is_exists_file(ppath.get_chapter_path(fname))


def is_exists_the_episode(fname: str) -> bool:
    """Check if the episode file exists."""
    return _is_exists_file(ppath.get_episode_path(fname))


def is_exists_the_event(fname: str) -> bool:
    """Check if the event file exists."""
    return _is_exists_file(ppath.get_event_path(fname))


def is_exists_the_item(fname: str) -> bool:
    """Check if the item file exists."""
    return _is_exists_file(ppath.get_item_path(fname))


def is_exists_the_note(fname: str) -> bool:
    """Check if the note file exists."""
    return _is_exists_file(ppath.get_note_path(fname))


def is_exists_the_outline(fname: str) -> bool:
    """Check if the outline file exists."""
    return _is_exists_file(ppath.get_outline_path(fname))


def is_exists_the_person(fname: str) -> bool:
    """Check if the person file exists."""
    return _is_exists_file(ppath.get_person_path(fname))


def is_exists_the_plan(fname: str) -> bool:
    """Check if the plan file exists."""
    return _is_exists_file(ppath.get_plan_path(fname))


def is_exists_the_scene(fname: str) -> bool:
    """Check if the scene file exists."""
    return _is_exists_file(ppath.get_scene_path(fname))


def is_exists_the_stage(fname: str) -> bool:
    """Check if the stage file exists."""
    return _is_exists_file(ppath.get_stage_path(fname))


def is_exists_the_word(fname: str) -> bool:
    """Check if the word file exists."""
    return _is_exists_file(ppath.get_word_path(fname))


def is_invalid_filename(fname: str) -> bool:
    """Check if the filaname is safe."""
    if not fname:
        return True
    else:
        return not isinstance(fname, str)


# Private Functions
def _exists_any_file(dirname: str, ext: str) -> bool:
    return len(glob.glob(os.path.join(dirname, f"*.{ext}"))) > 0


def _is_exists_file(filepath: str) -> bool:
    return os.path.exists(filepath)
