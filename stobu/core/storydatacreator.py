"""Story data create module for storybuilder."""


# Official Libraries


# My Modules
from stobu.dataconverter import conv_to_story_record
from stobu.datatypes import StoryData
from stobu.util import assertion
from stobu import projectpathmanager as ppath
from stobu.util.fileio import read_file_as_markdown, read_file_as_yaml
from stobu.util.log import logger


__all__ = (
        'get_story_data',
        )


# Main Function
def get_story_data(output_part: str) -> StoryData:
    logger.debug("Creating the story data...")
    logger.info(">> %s", output_part)

    order_data = assertion.is_dict(read_file_as_yaml(ppath.get_order_path()))

    part_data = _get_part_output(output_part)

    serialized = assertion.is_list(
            _serialized_file_names_from_order(
                order_data,
                part_data['ch'][0],
                part_data['ch'][1],
                part_data['ep'][0],
                part_data['ep'][1],
                part_data['sc'][0],
                part_data['sc'][1]))

    story_data = assertion.is_list(
            _conv_story_data_from_serialized_order_data(serialized))

    return StoryData(story_data)


# Private Function
def _conv_story_data_from_serialized_order_data(serialized: list) -> list:
    tmp = []

    tmp.append(conv_to_story_record('book/book', read_file_as_yaml(ppath.get_book_path())))

    for fname in serialized:
        tmp.append(conv_to_story_record(
            fname,
            _get_data_from_ordername(fname)))
    return tmp


def _get_data_from_ordername(ordername: str) -> dict:
    assert isinstance(ordername, str)

    category, fname = ordername.split('/')

    if category == 'chapter':
        tmp = read_file_as_yaml(ppath.get_chapter_path(fname))
        return tmp
    elif category == 'episode':
        tmp = read_file_as_yaml(ppath.get_episode_path(fname))
        return tmp
    elif category == 'scene':
        tmp = read_file_as_markdown(ppath.get_scene_path(fname))
        return tmp
    else:
        return {}


def _get_part_output(output_part: str) -> dict:
    assert isinstance(output_part, str)

    MAX = 100000
    part = output_part.split(':')
    tmp = {
            'ch': [0, MAX],
            'ep': [0, MAX],
            'sc': [0, MAX],
            }
    key = ''
    for p in part:
        if p in ('c', 'ch'):
            key = 'ch'
        elif p in ('e', 'ep'):
            key = 'ep'
        elif p in ('s', 'sc'):
            key = 'sc'
        else:
            continue
    if key:
        _, start, end = "", "", ""
        if len(output_part) > 3:
            _, start, end = output_part.split(':')
        else:
            _, start = output_part.split(':')
            end = -1
        _start = 0 if int(start) < 0 else int(start)
        _end = MAX if int(end) < 0 else int(end)
        tmp[key] = [_start, _end]
    return tmp


def _serialized_file_names_from_order(order_data: dict,
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

    if not order_data['book']:
        return []

    tmp = []
    ch_idx, ep_idx, sc_idx = 0, 0, 0

    for ch_record in assertion.is_list(order_data['book']):
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
    logger.info("## %s", tmp)
    return tmp
