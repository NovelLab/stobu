"""Common count module."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.utils.log import logger


__all__ = (
        'count_line_by_columns',
        'count_white_space',
        )


# Define Constants
PROC = 'COMMON COUNTS'


# Main
def count_line_by_columns(text: str, columns: int) -> float:
    assert isinstance(text, str)
    assert isinstance(columns, int)

    lines = text.split('\n')
    num = 0.0
    for line in lines:
        if len(line) > columns:
            num += len(line) / columns
        else:
            num += 1
    return num


def count_white_space(text: str) -> int:
    assert isinstance(text, str)

    space = 0
    for c in text:
        if c.isspace():
            space += 1
    return space
