"""Check module for build type."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.types.build import BuildType


__all__ = (
        'has_build_of',
        )



# Main
def has_build_of(args: Namespace, build: BuildType) -> bool:
    assert isinstance(args, Namespace)
    assert isinstance(build, BuildType)

    if BuildType.NOVEL is build:
        return args.novel
    elif BuildType.OUTLINE is build:
        return args.outline
    elif BuildType.PLOT is build:
        return args.plot
    elif BuildType.SCRIPT is build:
        return args.script
    elif BuildType.STRUCT is build:
        return args.struct
    else:
        return False
