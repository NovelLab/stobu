"""Utility module for list."""


# Official Libraries


# My Modules


__all__ = (
        'difference_list_from',
        )


# Main Functions
def difference_list_from(a: list, b: list) -> list:
    assert isinstance(a, list)
    assert isinstance(b, list)

    return list(set(a) - set(b))
