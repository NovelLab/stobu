"""Name tag DB manager for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.util.log import logger


class NameTagDB(object):

    """Name tag DB."""

    def __init__(self):
        self.tags = {}

    @classmethod
    def get_calling_tags(cls) -> dict:
        from storybuilder.util.filepath import basename_of
        from storybuilder.util.fileio import read_file_as_yaml
        from storybuilder.projectpathmanager import get_person_file_paths
        tmp = {}
        persons = get_person_file_paths()

        for fname in persons:
            data = read_file_as_yaml(fname)
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

