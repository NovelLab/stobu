"""Utility moducle for strings."""


# Official Libraries
from unicodedata import east_asian_width


# My Modules


__all__ = (
        'just_string_of',
        'rid_rn',
        )


# Define constants
ZEN = "".join(chr(0xff01 + i) for i in range(94))
"""string table for Zenkaku."""

HAN = "".join(chr(0x21 + i) for i in range(94))
"""string table for Hankaku."""

ZEN2HAN = str.maketrans(ZEN, HAN)
"""translate method."""

HAN2ZEN = str.maketrans(HAN, ZEN)
"""translate method."""


# Main Functions
def count_of_multibyte_strings(text: str) -> int:
    assert isinstance(text, str)

    count = 0
    for c in text:
        if east_asian_width(c) in 'FWA':
            count += 1
    return count


def count_of_singlebyte_strings(text: str) -> int:
    assert isinstance(text, str)

    count = 0
    for c in text:
        if east_asian_width(c) not in 'FWA':
            count += 1
    return count


def get_east_asian_width_count(text: str) -> int:
    assert isinstance(text, str)

    count = 0
    for c in text:
        if east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


def get_limit_string_east_asian_width(text: str, limit: int) -> str:
    assert isinstance(text, str)
    assert isinstance(limit, int)

    tmp = []
    idx = 0
    for c in text:
        if east_asian_width(c) in 'FWA':
            idx += 2
        else:
            idx += 1
        if idx <= limit:
            tmp.append(c)
    return "".join(tmp)


def hankaku_to_zenkaku(text: str) -> str:
    assert isinstance(text, str)

    return text.translate(HAN2ZEN)


def just_string_of(text: str, limit: int, padding: str = ' ', is_right: bool=False) -> str:
    assert isinstance(text, str)
    assert isinstance(limit, int)
    assert isinstance(padding, str)
    assert isinstance(is_right, bool)

    total_length = get_east_asian_width_count(text)
    if total_length > limit:
        return get_limit_string_east_asian_width(text, limit)
    else:
        multi = count_of_multibyte_strings(text) * 2
        single = count_of_singlebyte_strings(text)
        padding_num = limit - (single + multi)
        _padding = padding * padding_num
        return _padding + text if is_right else text + _padding


def rid_rn(src: str) -> str:
    '''Ridding linebreak mark from strings.'''
    assert isinstance(src, str)

    return src.rstrip('\r\n')
