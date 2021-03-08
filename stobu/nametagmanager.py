"""Name tag DB manager for storybuilder project."""


# Official Libraries


# My Modules
from stobu.tools import pathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import read_file_as_auto
from stobu.util.filepath import basename_of
from stobu.util.log import logger


class NameTagDB(object):

    """Name tag DB."""

    def __init__(self):
        self.tags = {}

    # class Methods
    @classmethod
    def get_calling_tags(cls) -> dict:
        tmp = {}
        persons = ppath.get_person_file_paths()

        for fname in persons:
            data = read_file_as_auto(fname)
            tmp[basename_of(fname)] = data['calling']
        return tmp

    # methods
    def add_item(self, key: str, name: str) -> bool:
        assert isinstance(key, str)
        assert isinstance(name, str)

        return self._add_name_to_tagdb(key, name) \
                and self._add_name_to_tagdb(self._add_prefix_name('i_', key), name)

    def add_person(self, key: str, name: str, fullname: str) -> bool:
        assert isinstance(key, str)
        assert isinstance(name, str)
        assert isinstance(fullname, str)

        return self._add_name_to_tagdb(key, name) \
                and self._add_name_to_tagdb(self._add_prefix_name('n_', key), name) \
                and self._add_name_to_tagdb(self._add_prefix_name('fn_', key), name) \
                and self._add_name_to_tagdb(self._add_prefix_name('ln_', key), name) \
                and self._add_name_to_tagdb(self._add_prefix_name('full_', key), name) \
                and self._add_name_to_tagdb(self._add_prefix_name('efull_', key), name)

    def add_stage(self, key: str, name: str) -> bool:
        assert isinstance(key, str)
        assert isinstance(name, str)

        return self._add_name_to_tagdb(key, name) \
                and self._add_name_to_tagdb(self._add_prefix_name('t_', key), name)

    def add_word(self, key: str, name: str) -> bool:
        assert isinstance(key, str)
        assert isinstance(name, str)

        return self._add_name_to_tagdb(key, name) \
                and self._add_name_to_tagdb(self._add_prefix_name('w_', key), name)

    def sort_db(self) -> bool:
        self.tags = dict(sorted(self.tags.items()))
        return True

    # private methods
    def _add_name_to_tagdb(self, key: str, name: str) -> bool:
        assert isinstance(key, str)
        assert isinstance(name, str)

        self.tags[key] = name
        return True

    def _add_prefix_name(self, prefix: str, key: str) -> str:
        assert isinstance(prefix, str)
        assert isinstance(key, str)

        return f"{prefix}{key}"


# Functions
def get_nametag_db() -> dict:
    logger.debug("Creating Name tag DB...")
    db = NameTagDB()

    logger.debug("> word names to DB")
    if not _create_nametags_from_word_files(db):
        return {}

    logger.debug("> item names to DB")
    if not _create_nametags_from_item_files(db):
        return {}

    logger.debug("> stage names to DB")
    if not _create_nametags_from_stage_files(db):
        return {}

    logger.debug("> person names to DB")
    if not _create_nametags_from_person_files(db):
        return {}

    if not db.sort_db():
        logger.error("Failed to sort DB!")
        return {}

    logger.debug("...Succeeded create name tag DB.")
    return db.tags


# Private Functions
def _create_nametags_from_item_files(db: NameTagDB) -> bool:
    items = ppath.get_item_file_paths()
    for fname in assertion.is_list(items):
        data = assertion.is_dict(read_file_as_auto(fname))
        if not db.add_item(basename_of(fname), data['name']):
            logger.error("Failed to add an item name to tag DB!")
            return False
    return True


def _create_nametags_from_person_files(db: NameTagDB) -> bool:
    persons = ppath.get_person_file_paths()
    for fname in assertion.is_list(persons):
        data = assertion.is_dict(read_file_as_auto(fname))
        if not db.add_person(basename_of(fname), data['name'], data['fullname']):
            logger.error("Failed to add a person name to tag DB!")
            return False
    return True


def _create_nametags_from_stage_files(db: NameTagDB) -> bool:
    stages = ppath.get_stage_file_paths()
    for fname in assertion.is_list(stages):
        data = assertion.is_dict(read_file_as_auto(fname))
        if not db.add_stage(basename_of(fname), data['name']):
            logger.error("Failed to add a stage name to tag DB!")
            return False
    return True


def _create_nametags_from_word_files(db: NameTagDB) -> bool:
    words = ppath.get_word_file_paths()
    for fname in assertion.is_list(words):
        data = assertion.is_dict(read_file_as_auto(fname))
        if not db.add_word(basename_of(fname), data['name']):
            logger.error("Failed to add a word name to tag DB!")
            return False
    return True
