"""Utility module for file paths."""

# Official Libraries
import os


__all__ = (
        'basename_of',
        'filename_with_number',
        'new_filename_by_input',
        )


# Main
def basename_of(filepath: str) -> str:
    assert isinstance(filepath, str)

    return os.path.splitext(os.path.basename(filepath))[0]


def filenames_with_number(fnames: list, first_num: int = 1) -> list:
    assert isinstance(fnames, list)
    assert isinstance(first_num, int)

    tmp = []
    idx = first_num

    for fname in fnames:
        assert isinstance(fname, str)
        tmp.append(f"{idx}: {fname}")
        idx += 1
    return tmp


def new_filename_by_input(title: str) -> str:
    assert isinstance(title, str)

    return input(f"> Please Enter the new file name of {title}: ")
