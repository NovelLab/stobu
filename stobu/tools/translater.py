"""Translate tag module."""

# Official Libraries
import re


# My Modules
from stobu.syss import messages as msg
from stobu.utils.log import logger


__all__ = (
        'translate_tags_str',
        'translate_tags_text_list',
        )


# Define Constants
PROC = 'TRANSLATE TAG'


# Main
def translate_tags_str(text: str, tags: dict) -> str:
    assert isinstance(text, str)
    assert isinstance(tags, dict)

    return _conv_text_by_tag(text, tags)


def translate_tags_text_list(textlist: list, tags: dict) -> list:
    assert isinstance(textlist, list)
    assert isinstance(tags, dict)

    tmp = []

    for text in textlist:
        assert isinstance(text, str)
        tmp.append(_conv_text_by_tag(text, tags))

    return tmp


# Private Functions
def _conv_text_by_tag(text: str, tags: dict, prefix: str = '$') -> str:
    assert isinstance(text, str)
    assert isinstance(tags, dict)

    tmp = text

    for key, val in tags.items():
        if prefix in tmp:
            tag_key = f"{prefix}{key}"
            if tag_key in tmp:
                if prefix:
                    tmp = re.sub(r'\{}{}'.format(prefix, key), val, tmp)
                else:
                    tmp = re.sub(key, val, tmp)
    return tmp
