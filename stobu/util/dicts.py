"""Utility module for dictonary."""


# Official Libraries


# My Modules


__all__ = (
        'dict_sorted',
        )


# Main Functions
def dict_sorted(src: dict, is_reverse: bool=False) -> dict:
    """Convert the dictionary data to sorted data."""
    assert isinstance(src, dict)
    assert isinstance(is_reverse, bool)

    return dict(sorted(src.items(), key=lambda x: x[0], reverse=is_reverse))
