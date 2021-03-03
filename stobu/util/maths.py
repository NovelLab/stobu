"""Math utility module."""


# Official Libraries


# My Modules


__all__ = (
        'int_ceil',
        )


# Main Functions
def int_ceil(a: int, b: int) -> int:
    ''' Ceil integer'''
    assert isinstance(a, int)
    assert isinstance(b, int)
    return -(-a // b)


def safe_divided(a: (int, float), b: (int, float)) -> (int, float):
    ''' Except zero divide'''
    assert isinstance(a, (int, float))
    assert isinstance(b, (int, float))

    return a / b if b else 0
