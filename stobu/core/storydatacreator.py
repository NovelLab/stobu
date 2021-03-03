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
def get_story_data() -> StoryData:
    logger.debug("Creating the story data...")

    order_data = assertion.is_dict(read_file_as_yaml(ppath.get_order_path()))

    serialized = assertion.is_list(_serialized_file_names_from_order(order_data))

    story_data = assertion.is_list(_conv_story_data_from_serialized_order_data(serialized))

    logger.debug("...Succeeded create the story data.")
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


def _serialized_file_names_from_order(order_data: dict) -> list:
    assert isinstance(order_data, dict)

    tmp = []

    for ch_record in assertion.is_list(order_data['book']):
        assert isinstance(ch_record, dict)
        for key in ch_record.keys():
            tmp.append(key)
        for ch_data in ch_record.values():
            assert isinstance(ch_data, list)
            for ep_record in ch_data:
                assert isinstance(ep_record, dict)
                for key in ep_record.keys():
                    tmp.append(key)
                for ep_data in ep_record.values():
                    assert isinstance(ep_data, list)
                    for sc_record in ep_data:
                        assert isinstance(sc_record, str)
                        tmp.append(sc_record)
    return tmp
