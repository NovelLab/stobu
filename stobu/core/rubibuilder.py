"""Rubi module for storybuilder."""


# Official Libraries
import re


# My Modules
from stobu import projectpathmanager as ppath
from stobu.util import assertion
from stobu.util.fileio import read_file_as_yaml


__all__ = (
        'apply_rubi_convert',
        )


# Main Functions
def apply_rubi_convert(output_data: list) -> list:
    assert isinstance(output_data, list)

    rubi = assertion.is_dict(read_file_as_yaml(ppath.get_rubi_path()))

    tmp = []
    discards = []

    for line in output_data:
        assert isinstance(line, str)
        if line.startswith('#') or line.startswith('**') or line == '\n':
            tmp.append(line)
            continue
        for key in rubi.keys():
            if key in discards:
                continue
            elif _has_rubi_key(line, key):
                if _has_rubi_exclusions(line, rubi[key]['exclusions']):
                    continue
                line = _add_rubi(line, key, rubi[key]['rubi'])
                if not rubi[key]['always']:
                    discards.append(key)
        tmp.append(line)
    return tmp


# Private Functions
def _add_rubi(src: str, key: str, rubi: str, num: int = 1) -> str:
    assert isinstance(src, str)
    assert isinstance(key, str)
    assert isinstance(rubi, str)
    assert isinstance(num, int)

    return re.sub(r'{}'.format(key), r'{}'.format(rubi), src, num)


def _has_rubi_exclusions(src: str, ex_words: list) -> bool:
    assert isinstance(src, str)
    assert isinstance(ex_words, list)

    for word in ex_words:
        assert isinstance(word, str)
        if word in src:
            return True
    return False


def _has_rubi_key(src: str, key: str) -> bool:
    assert isinstance(src, str)
    assert isinstance(key, str)

    return True if re.search(r'{}'.format(key), src) else False
