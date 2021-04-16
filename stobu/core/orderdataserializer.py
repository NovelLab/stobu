"""Order data serialize module."""

# Official Libraries


# My Modules
from stobu.elms.orders import OrderItem
from stobu.syss import messages as msg
from stobu.utils import assertion
from stobu.utils.log import logger


__all__ = (
        'serialized_filenames_from_order',
        )


# Define Constants
PROC = 'ORDER SERIALIZER'


# Main
def serialized_filenames_from_order(order_data: dict,
        ch_start: int, ch_end: int,
        ep_start: int, ep_end: int,
        sc_start: int, sc_end: int) -> list:
    assert isinstance(order_data, dict)
    assert isinstance(ch_start, int)
    assert isinstance(ch_end, int)
    assert isinstance(ep_start, int)
    assert isinstance(ep_end, int)
    assert isinstance(sc_start, int)
    assert isinstance(sc_end, int)

    logger.debug(msg.PROC_START.format(proc=PROC))

    if not _is_valid_order_data(order_data):
        logger.error(msg.ERR_FAIL_INVALID_DATA.format(proc=f"order data: {PROC}"))
        return []

    tmp = []
    ch_idx, ep_idx, sc_idx = 0, 0, 0

    for ch_record in assertion.is_list(order_data[str(OrderItem.BOOK)]):
        assert isinstance(ch_record, dict)
        if ch_start > ch_idx or ch_idx > ch_end:
            ch_idx += 1
            continue
        for key in ch_record.keys():
            tmp.append(key)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                if ep_start > ep_idx or ep_idx > ep_end:
                    ep_idx += 1
                    continue
                for key in ep_record.keys():
                    tmp.append(key)
                for ep_data in ep_record.values():
                    assert isinstance(ep_data, list)
                    for sc_record in ep_data:
                        assert isinstance(sc_record, str)
                        if sc_start > sc_idx or sc_idx > sc_end:
                            sc_idx += 1
                            continue
                        tmp.append(sc_record)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


# Private Functions
def _is_valid_order_data(data: dict) -> bool:
    assert isinstance(data, dict)

    return str(OrderItem.BOOK) in data
