"""Read order data module."""

# Official Libraries
import yaml


# My Modules
from stobu.elms.orders import OrderItem
from stobu.syss import messages as msg
from stobu.tools.pathgetter import filepath_of
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.fileio import read_file
from stobu.utils.filepath import basename_of
from stobu.utils.log import logger


__all__ = (
        'elm_from_ordername',
        'get_order_data',
        'get_filenames_in_order_by_elm',
        'get_chapters_in_order',
        'get_episodes_in_order',
        'get_scenes_in_order',
        'ordername_of',
        'orderitem_of',
        'rid_prefix',
        'get_parent_item_of',
        'get_elm_from_order',
        )


# Define Constants
PROC = 'TOOL ORDER DATA READER'


ORDER_ITEM_TABLE = {
        ElmType.BOOK: OrderItem.BOOK,
        ElmType.CHAPTER: OrderItem.CHAPTER,
        ElmType.EPISODE: OrderItem.EPISODE,
        ElmType.SCENE: OrderItem.SCENE,
        }


ELM_ITEM_TABLE = {
        OrderItem.BOOK: ElmType.BOOK,
        OrderItem.CHAPTER: ElmType.CHAPTER,
        OrderItem.EPISODE: ElmType.EPISODE,
        OrderItem.SCENE: ElmType.SCENE,
        }


# Main
def elm_from_ordername(ordername: str) -> ElmType:
    assert isinstance(ordername, str)

    if str(OrderItem.BOOK) in ordername:
        return ElmType.BOOK
    elif str(OrderItem.CHAPTER) in ordername:
        return ElmType.CHAPTER
    elif str(OrderItem.EPISODE) in ordername:
        return ElmType.EPISODE
    elif str(OrderItem.SCENE) in ordername:
        return ElmType.SCENE
    else:
        logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"in {PROC}"))
        return ElmType.NONE


def get_filenames_in_order_by_elm(elm: ElmType) -> list:
    assert isinstance(elm, ElmType)

    if ElmType.CHAPTER is elm:
        return get_chapters_in_order()
    elif ElmType.EPISODE is elm:
        return get_episodes_in_order()
    elif ElmType.SCENE is elm:
        return get_scenes_in_order()
    else:
        return []


def get_chapters_in_order() -> list:
    data = assertion.is_list(get_order_data()[str(OrderItem.BOOK)])
    tmp = []

    for ch_record in data:
        assert isinstance(ch_record, dict)
        for key in ch_record.keys():
            if str(OrderItem.CHAPTER) in key:
                tmp.append(rid_prefix(OrderItem.CHAPTER, key))
    return tmp


def get_elm_from_order(item: OrderItem) -> ElmType:
    assert isinstance(item, OrderItem)

    return ELM_ITEM_TABLE[item]


def get_episodes_in_order() -> list:
    data = assertion.is_list(get_order_data()[str(OrderItem.BOOK)])
    tmp = []

    for ch_record in data:
        assert isinstance(ch_record, dict)
        for ep_data in ch_record.values():
            assert isinstance(ep_data, list)
            for ep_record in ep_data:
                assert isinstance(ep_record, dict)
                for key in ep_record.keys():
                    if str(OrderItem.EPISODE) in key:
                        tmp.append(rid_prefix(OrderItem.EPISODE, key))
    return tmp


def get_order_data() -> dict:
    data = read_file(filepath_of(ElmType.ORDER, ''))

    return yaml.safe_load(data)


def get_parent_item_of(item: OrderItem) -> OrderItem:
    assert isinstance(item, OrderItem)

    if OrderItem.BOOK is item:
        return OrderItem.BOOK
    elif OrderItem.CHAPTER is item:
        return OrderItem.BOOK
    elif OrderItem.EPISODE is item:
        return OrderItem.CHAPTER
    elif OrderItem.SCENE is item:
        return OrderItem.EPISODE
    else:
        return OrderItem.BOOK


def get_scenes_in_order() -> list:
    data = assertion.is_list(get_order_data()[str(OrderItem.BOOK)])
    tmp = []

    for ch_record in data:
        assert isinstance(ch_record, dict)
        for ep_data in ch_record.values():
            assert isinstance(ep_data, list)
            for ep_record in ep_data:
                assert isinstance(ep_record, dict)
                for sc_data in ep_record.values():
                    assert isinstance(sc_data, list)
                    for sc_record in sc_data:
                        assert isinstance(sc_record, str)
                        if str(OrderItem.SCENE) in sc_record:
                            tmp.append(rid_prefix(OrderItem.SCENE, sc_record))
    return tmp


def ordername_of(item: OrderItem, fname: str) -> str:
    assert isinstance(item, OrderItem)
    assert isinstance(fname, str)

    if OrderItem.BOOK is item:
        return str(OrderItem.BOOK)
    else:
        return f"{str(item)}{basename_of(fname)}"


def orderitem_of(elm: ElmType) -> OrderItem:
    assert isinstance(elm, ElmType)

    return ORDER_ITEM_TABLE[elm]


def rid_prefix(item: OrderItem, title: str) -> str:
    assert isinstance(item, OrderItem)
    assert isinstance(title, str)

    return title.replace(str(item), '')


# Private Functions
