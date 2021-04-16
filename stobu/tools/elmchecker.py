"""Check element module."""

# Official Libraries
from argparse import Namespace


# My Modules
from stobu.types.element import ElmType


__all__ = (
        'has_elm_of',
        'is_enable_elm_in',
        'is_enable_the_elm',
        )


# Define Constants
ELM_TABLE = {
        ElmType.BOOK: ('book'),
        ElmType.BUILD: ('build'),
        ElmType.CHAPTER: ('c', 'chapter'),
        ElmType.EPISODE: ('e', 'episode'),
        ElmType.EVENT: ('v', 'event'),
        ElmType.ITEM: ('i', 'item'),
        ElmType.MATERIAL: ('material'),
        ElmType.MOB: ('mob'),
        ElmType.NONE: ('none'),
        ElmType.NOTE: ('n', 'note'),
        ElmType.ORDER: ('order'),
        ElmType.OUTLINE: ('o', 'outline'),
        ElmType.PERSON: ('p', 'person'),
        ElmType.PLAN: ('l', 'plan'),
        ElmType.PLOT: ('plot'),
        ElmType.PROJECT: ('project'),
        ElmType.RUBI: ('rubi'),
        ElmType.SCENE: ('s', 'scene'),
        ElmType.STAGE: ('t', 'stage'),
        ElmType.TIME: ('time'),
        ElmType.TODO: ('todo'),
        ElmType.TRASH: ('trash'),
        ElmType.WORD: ('w', 'word'),
        }


# Main
def elm_from(args: Namespace) -> ElmType:
    assert isinstance(args, Namespace)

    for elm, checker in ELM_TABLE.items():
        if args.elm in checker:
            return elm
    return ElmType.NONE


def has_elm_of(args: Namespace, elm: ElmType) -> bool:
    assert isinstance(args, Namespace)
    assert isinstance(elm, ElmType)

    order_elm = args.arg0

    return order_elm in ELM_TABLE[elm]


def is_enable_elm_in(args: Namespace, enables: list) -> bool:
    assert isinstance(args, Namespace)
    assert isinstance(enables, list)

    order_elm = elm_from(args)

    return is_enable_the_elm(order_elm, enables)


def is_enable_the_elm(elm: ElmType, enables: list) -> bool:
    assert isinstance(elm, ElmType)
    assert isinstance(enables, list)

    for enable in enables:
        if elm is enable:
            return True
    return False
