"""Utility moducle for strings."""


# Official Libraries


# My Modules


__all__ = (
        'rid_rn',
        )


# Main Functions
def rid_rn(src: str) -> str:
    assert isinstance(src, str)
    return src.rstrip('\r\n')
