"""Management storybuilder's project paths."""


# Official Libraries
import glob
import os


# My Modules
from stobu.systems.settings import PROJECT_FILENAME, BOOK_FILENAME, ORDER_FILENAME
from stobu.systems.settings import RUBI_FILENAME, TODO_FILENAME, TIME_FILENAME, MOB_FILENAME
from stobu.systems.settings import CHAPTER_DIR, EPISODE_DIR, SCENE_DIR, NOTE_DIR
from stobu.systems.settings import PERSON_DIR, STAGE_DIR, ITEM_DIR, WORD_DIR
from stobu.systems.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT
from stobu.systems.settings import PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.systems.settings import TRASH_DIR, BUILD_DIR
from stobu.systems.settings import PLAN_DIR, OUTLINE_DIR, EVENT_DIR
from stobu.systems.settings import PLAN_EXT, OUTLINE_EXT, EVENT_EXT
from stobu.util.filepath import add_extention, basename_of


__all__ = (
        'get_current_path',
        'get_book_path',
        'get_order_path',
        'get_project_path',
        'get_rubi_path',
        'get_todo_path',
        'get_time_path',
        'get_mob_path',
        'get_build_dir_path',
        'get_trash_dir_path', 'get_trash_file_paths', 'get_trash_file_names',
        'get_plan_path', 'get_plan_dir_path', 'get_plan_file_paths', 'get_plan_file_names',
        'get_outline_path', 'get_outline_dir_path', 'get_outline_file_paths', 'get_outline_file_names',
        'get_event_path', 'get_event_dir_path', 'get_event_file_paths', 'get_event_file_names',
        'get_chapter_path', 'get_chapter_dir_path', 'get_chapter_file_paths', 'get_chapter_file_names',
        'get_episode_path', 'get_episode_dir_path', 'get_episode_file_paths', 'get_episode_file_names',
        'get_scene_path', 'get_scene_dir_path', 'get_scene_file_paths', 'get_scene_file_names',
        'get_note_path', 'get_note_dir_path', 'get_note_file_paths', 'get_note_file_names',
        'get_person_path', 'get_person_dir_path', 'get_person_file_paths', 'get_person_file_names',
        'get_stage_path', 'get_stage_dir_path', 'get_stage_file_paths', 'get_stage_file_names',
        'get_item_path', 'get_item_dir_path', 'get_item_file_paths', 'get_item_file_names',
        'get_word_path', 'get_word_dir_path', 'get_word_file_paths', 'get_word_file_names',
        )


# Main Functions
def get_book_path() -> str:
    return os.path.join(get_current_path(), BOOK_FILENAME)


def get_build_dir_path() -> str:
    return os.path.join(get_current_path(), BUILD_DIR)


def get_chapter_dir_path() -> str:
    return os.path.join(get_current_path(), CHAPTER_DIR)


def get_chapter_file_names() -> list:
    return _get_any_file_names(get_chapter_file_paths())


def get_chapter_file_paths() -> list:
    return _get_any_file_paths(get_chapter_dir_path(), CHAPTER_EXT)


def get_chapter_path(fname: str) -> str:
    return os.path.join(get_chapter_dir_path(), _get_any_path(fname, CHAPTER_EXT))


def get_episode_dir_path() -> str:
    return os.path.join(get_current_path(), EPISODE_DIR)


def get_episode_file_names() -> list:
    return _get_any_file_names(get_episode_file_paths())


def get_episode_file_paths() -> list:
    return _get_any_file_paths(get_episode_dir_path(), EPISODE_EXT)


def get_episode_path(fname: str) -> str:
    return os.path.join(get_episode_dir_path(), _get_any_path(fname, EPISODE_EXT))


def get_event_dir_path() -> str:
    return os.path.join(get_current_path(), EVENT_DIR)


def get_event_file_names() -> list:
    return _get_any_file_names(get_event_file_paths())


def get_event_file_paths() -> list:
    return _get_any_file_paths(get_event_dir_path(), EVENT_EXT)


def get_event_path(fname: str) -> str:
    return os.path.join(get_event_dir_path(), _get_any_path(fname, EVENT_EXT))


def get_current_path() -> str:
    return os.getcwd()


def get_item_dir_path() -> str:
    return os.path.join(get_current_path(), ITEM_DIR)


def get_item_file_names() -> list:
    return _get_any_file_names(get_item_file_paths())


def get_item_file_paths() -> list:
    return _get_any_file_paths(get_item_dir_path(), ITEM_EXT)


def get_item_path(fname: str) -> str:
    return os.path.join(get_item_dir_path(), _get_any_path(fname, ITEM_EXT))


def get_mob_path() -> str:
    return os.path.join(get_current_path(), MOB_FILENAME)


def get_note_dir_path() -> str:
    return os.path.join(get_current_path(), NOTE_DIR)


def get_note_file_names() -> list:
    return _get_any_file_names(get_note_file_paths())


def get_note_file_paths() -> list:
    return _get_any_file_paths(get_note_dir_path(), NOTE_EXT)


def get_note_path(fname: str) -> str:
    return os.path.join(get_note_dir_path(), _get_any_path(fname, NOTE_EXT))


def get_order_path() -> str:
    return os.path.join(get_current_path(), ORDER_FILENAME)


def get_outline_dir_path() -> str:
    return os.path.join(get_current_path(), OUTLINE_DIR)


def get_outline_file_names() -> list:
    return _get_any_file_names(get_outline_file_paths())


def get_outline_file_paths() -> list:
    return _get_any_file_paths(get_outline_dir_path(), OUTLINE_EXT)


def get_outline_path(fname: str) -> str:
    return os.path.join(get_outline_dir_path(), _get_any_path(fname, OUTLINE_EXT))


def get_person_dir_path() -> str:
    return os.path.join(get_current_path(), PERSON_DIR)


def get_person_file_names() -> list:
    return _get_any_file_names(get_person_file_paths())


def get_person_file_paths() -> list:
    return _get_any_file_paths(get_person_dir_path(), PERSON_EXT)


def get_person_path(fname: str) -> str:
    return os.path.join(get_person_dir_path(), _get_any_path(fname, PERSON_EXT))


def get_plan_dir_path() -> str:
    return os.path.join(get_current_path(), PLAN_DIR)


def get_plan_file_names() -> list:
    return _get_any_file_names(get_plan_file_paths())


def get_plan_file_paths() -> list:
    return _get_any_file_paths(get_plan_dir_path(), PLAN_EXT)


def get_plan_path(fname: str) -> str:
    return os.path.join(get_plan_dir_path(), _get_any_path(fname, PLAN_EXT))


def get_project_path() -> str:
    return os.path.join(get_current_path(), PROJECT_FILENAME)


def get_rubi_path() -> str:
    return os.path.join(get_current_path(), RUBI_FILENAME)


def get_scene_dir_path() -> str:
    return os.path.join(get_current_path(), SCENE_DIR)


def get_scene_file_names() -> list:
    return _get_any_file_names(get_scene_file_paths())


def get_scene_file_paths() -> list:
    return _get_any_file_paths(get_scene_dir_path(), SCENE_EXT)


def get_scene_path(fname: str) -> str:
    return os.path.join(get_scene_dir_path(), _get_any_path(fname, SCENE_EXT))


def get_stage_dir_path() -> str:
    return os.path.join(get_current_path(), STAGE_DIR)


def get_stage_file_names() -> list:
    return _get_any_file_names(get_stage_file_paths())


def get_stage_file_paths() -> list:
    return _get_any_file_paths(get_stage_dir_path(), STAGE_EXT)


def get_stage_path(fname: str) -> str:
    return os.path.join(get_stage_dir_path(), _get_any_path(fname, STAGE_EXT))


def get_time_path() -> str:
    return os.path.join(get_current_path(), TIME_FILENAME)


def get_todo_path() -> str:
    return os.path.join(get_current_path(), TODO_FILENAME)


def get_trash_dir_path() -> str:
    return os.path.join(get_current_path(), TRASH_DIR)


def get_trash_file_names() -> list:
    return _get_any_file_names(get_trash_file_paths())


def get_trash_file_paths() -> list:
    return _get_any_file_paths(get_trash_dir_path(), CHAPTER_EXT) \
            + _get_any_file_paths(get_trash_dir_path(), SCENE_EXT)


def get_word_dir_path() -> str:
    return os.path.join(get_current_path(), WORD_DIR)


def get_word_file_names() -> list:
    return _get_any_file_names(get_word_file_paths())


def get_word_file_paths() -> list:
    return _get_any_file_paths(get_word_dir_path(), WORD_EXT)


def get_word_path(fname: str) -> str:
    return os.path.join(get_word_dir_path(), _get_any_path(fname, WORD_EXT))


# Private Functions
def _get_any_file_names(paths: list) -> list:
    assert isinstance(paths, list)

    return [basename_of(name) for name in paths]


def _get_any_file_paths(dirname: str, ext: str) -> list:
    assert isinstance(dirname, str)
    assert isinstance(ext, str)

    return sorted(glob.glob(os.path.join(dirname, f"*.{ext}")))


def _get_any_path(fname :str, ext: str) -> str:
    assert isinstance(fname, str)
    assert isinstance(ext, str)

    return add_extention(basename_of(fname), ext)
