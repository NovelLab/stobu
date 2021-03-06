"""Management storybuilder's project paths."""


# Official Libraries
import glob
import os


# My Modules
from stobu.settings import PROJECT_FILENAME, BOOK_FILENAME, ORDER_FILENAME
from stobu.settings import RUBI_FILENAME
from stobu.settings import CHAPTER_DIR, EPISODE_DIR, SCENE_DIR, NOTE_DIR
from stobu.settings import PERSON_DIR, STAGE_DIR, ITEM_DIR, WORD_DIR
from stobu.settings import CHAPTER_EXT, EPISODE_EXT, SCENE_EXT, NOTE_EXT
from stobu.settings import PERSON_EXT, STAGE_EXT, ITEM_EXT, WORD_EXT
from stobu.settings import TRASH_DIR, BUILD_DIR
from stobu.util.filepath import basename_of


__all__ = (
        'get_current_path',
        'get_book_path', 'get_order_path', 'get_project_path',
        'get_build_dir_path',
        'get_trash_dir_path', 'get_trash_file_paths', 'get_trash_file_names',
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
    return [basename_of(name) for name in get_chapter_file_paths()]


def get_chapter_file_paths() -> list:
    return _get_any_file_paths(get_chapter_dir_path(), CHAPTER_EXT)


def get_chapter_path(fname: str) -> str:
    return os.path.join(get_chapter_dir_path(),
                        f"{basename_of(fname)}.{CHAPTER_EXT}")


def get_episode_dir_path() -> str:
    return os.path.join(get_current_path(), EPISODE_DIR)


def get_episode_file_names() -> list:
    return [basename_of(name) for name in get_episode_file_paths()]


def get_episode_file_paths() -> list:
    return _get_any_file_paths(get_episode_dir_path(), EPISODE_EXT)


def get_episode_path(fname: str) -> str:
    return os.path.join(get_episode_dir_path(),
                        f"{basename_of(fname)}.{EPISODE_EXT}")


def get_current_path() -> str:
    return os.getcwd()


def get_item_dir_path() -> str:
    return os.path.join(get_current_path(), ITEM_DIR)


def get_item_file_names() -> list:
    return [basename_of(name) for name in get_item_file_paths()]


def get_item_file_paths() -> list:
    return _get_any_file_paths(get_item_dir_path(), ITEM_EXT)


def get_item_path(fname: str) -> str:
    return os.path.join(get_item_dir_path(),
                        f"{basename_of(fname)}.{ITEM_EXT}")


def get_note_dir_path() -> str:
    return os.path.join(get_current_path(), NOTE_DIR)


def get_note_file_names() -> list:
    return [basename_of(name) for name in get_note_file_paths()]


def get_note_file_paths() -> list:
    return _get_any_file_paths(get_note_dir_path(), NOTE_EXT)


def get_note_path(fname: str) -> str:
    return os.path.join(get_note_dir_path(),
                        f"{basename_of(fname)}.{NOTE_EXT}")


def get_order_path() -> str:
    return os.path.join(get_current_path(), ORDER_FILENAME)


def get_person_dir_path() -> str:
    return os.path.join(get_current_path(), PERSON_DIR)


def get_person_file_names() -> list:
    return [basename_of(name) for name in get_person_file_paths()]


def get_person_file_paths() -> list:
    return _get_any_file_paths(get_person_dir_path(), PERSON_EXT)


def get_person_path(fname: str) -> str:
    return os.path.join(get_person_dir_path(),
                        f"{basename_of(fname)}.{PERSON_EXT}")


def get_project_path() -> str:
    return os.path.join(get_current_path(), PROJECT_FILENAME)


def get_rubi_path() -> str:
    return os.path.join(get_current_path(), RUBI_FILENAME)


def get_scene_dir_path() -> str:
    return os.path.join(get_current_path(), SCENE_DIR)


def get_scene_file_names() -> list:
    return [basename_of(name) for name in get_scene_file_paths()]


def get_scene_file_paths() -> list:
    return _get_any_file_paths(get_scene_dir_path(), SCENE_EXT)


def get_scene_path(fname: str) -> str:
    return os.path.join(get_scene_dir_path(),
                        f"{basename_of(fname)}.{SCENE_EXT}")


def get_stage_dir_path() -> str:
    return os.path.join(get_current_path(), STAGE_DIR)


def get_stage_file_names() -> list:
    return [basename_of(name) for name in get_stage_file_paths()]


def get_stage_file_paths() -> list:
    return _get_any_file_paths(get_stage_dir_path(), STAGE_EXT)


def get_stage_path(fname: str) -> str:
    return os.path.join(get_stage_dir_path(),
                        f"{basename_of(fname)}.{STAGE_EXT}")


def get_trash_dir_path() -> str:
    return os.path.join(get_current_path(), TRASH_DIR)


def get_trash_file_names() -> list:
    return [basename_of(name) for name in get_trash_file_paths()]


def get_trash_file_paths() -> list:
    return _get_any_file_paths(get_trash_dir_path(), CHAPTER_EXT) \
            + _get_any_file_paths(get_trash_dir_path(), SCENE_EXT)


def get_word_dir_path() -> str:
    return os.path.join(get_current_path(), WORD_DIR)


def get_word_file_names() -> list:
    return [basename_of(name) for name in get_word_file_paths()]


def get_word_file_paths() -> list:
    return _get_any_file_paths(get_word_dir_path(), WORD_EXT)


def get_word_path(fname: str) -> str:
    return os.path.join(get_word_dir_path(),
                        f"{basename_of(fname)}.{WORD_EXT}")


# Private Functions
def _get_any_file_paths(dirname: str, ext: str) -> list:
    return sorted(glob.glob(os.path.join(dirname, f"*.{ext}")))
