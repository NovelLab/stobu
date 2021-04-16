"""Order data write module."""

# Official Libraries
import yaml


# My Modules
from stobu.elms.orders import OrderItem
from stobu.syss import messages as msg
from stobu.tools.orderdatareader import get_parent_item_of, ordername_of
from stobu.tools.pathgetter import filepath_of
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.fileio import read_file, write_file
from stobu.utils.filepath import basename_of
from stobu.utils.log import logger


__all__ = (
        'add_order_data',
        'remove_item_order_data',
        'write_order_data',
        )


# Main
def add_order_data(item: OrderItem, fname: str, parent: str) -> dict:
    assert isinstance(item, OrderItem)
    assert isinstance(fname, str)
    assert isinstance(parent, str)

    data = _get_order_raw_data()
    _fname = ordername_of(item, fname)
    _parent = ordername_of(get_parent_item_of(item), parent)

    if OrderItem.CHAPTER is item:
        assertion.is_list(data[str(OrderItem.BOOK)]).append({_fname: []})
        return data

    for ch_record in assertion.is_list(data[str(OrderItem.BOOK)]):
        assert isinstance(ch_record, dict)
        for ch_key, ch_data in ch_record.items():
            assert isinstance(ch_data, list)
            if OrderItem.EPISODE is item and ch_key == _parent:
                ch_data.append({_fname: []})
                return data

            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                for ep_key, ep_data in ep_record.items():
                    assert isinstance(ep_data, list)
                    if OrderItem.SCENE is item and ep_key == _parent:
                        ep_data.append(_fname)
                        return data
    return data


def remove_item_order_data(item: OrderItem, fname: str) -> dict:
    assert isinstance(item, OrderItem)
    assert isinstance(fname, str)

    data = assertion.is_dict(_get_order_raw_data())
    _fname = ordername_of(item, fname)

    if OrderItem.CHAPTER is item:
        if not _reject_chapter_from_order(data, _fname):
            logger.error(msg.ERR_FAIL_CANNOT_REMOVE_DATA.format(data=f"in {PROC}"))
        return data
    elif OrderItem.EPISODE is item:
        if not _reject_episode_from_order(data, _fname):
            logger.error(msg.ERR_FAIL_CANNOT_REMOVE_DATA.format(data=f"in {PROC}"))
        return data
    elif OrderItem.SCENE is item:
        if not _reject_scene_from_order(data, _fname):
            logger.error(msg.ERR_FAIL_CANNOT_REMOVE_DATA.format(data=f"in {PROC}"))
        return data
    else:
        return data


def write_order_data(orderdata: dict) -> bool:
    assert isinstance(orderdata, dict)
    assert str(OrderItem.BOOK) in orderdata

    if not write_file(filepath_of(ElmType.ORDER, ''), yaml.safe_dump(orderdata)):
        logger.error(msg.ERR_FAIL_CANNOT_WRITE_DATA.format(data=f"order data in {PROC}"))
        return False
    return True


# Private Functions
def _get_order_raw_data() -> dict:
    data = read_file(filepath_of(ElmType.ORDER, ''))
    return yaml.safe_load(data)


def _reject_chapter_from_order(orders: dict, fname: str) -> bool:
    assert isinstance(orders, dict)
    assert isinstance(fname, str)

    _ch_name = ordername_of(OrderItem.CHAPTER, fname)
    tmp = []

    for ch_record in assertion.is_list(orders[str(OrderItem.BOOK)]):
        assert isinstance(ch_record, dict)
        if _ch_name not in ch_record.keys():
            tmp.append(ch_record)
    orders[str(OrderItem.BOOK)] = tmp
    return True


def _reject_episode_from_order(orders: dict, fname: str) -> bool:
    assert isinstance(orders, dict)
    assert isinstance(fname, str)

    _ep_name = ordername_of(OrderItem.EPISODE, fname)

    for ch_record in assertion.is_list(orders[str(OrderItem.BOOK)]):
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            tmp = []
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                if _ep_name not in ep_record.keys():
                    tmp.append(ep_record)
            for key in ch_record.keys():
                ch_record[key] = tmp
    return True


def _reject_scene_from_order(orders: dict, fname: str) -> bool:
    assert isinstance(orders, dict)
    assert isinstance(fname, str)

    _sc_name = ordername_of(OrderItem.SCENE, fname)

    for ch_record in assertion.is_list(orders[str(OrderItem.BOOK)]):
        assert isinstance(ch_record, dict)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                for ep_data in ep_record.values():
                    assert isinstance(ep_data, list)
                    tmp = []
                    for sc_record in ep_data:
                        assert isinstance(sc_record, str)
                        if sc_record != _sc_name:
                            tmp.append(sc_record)
                    for key in ep_record.keys():
                        ep_record[key] = tmp
    return True
