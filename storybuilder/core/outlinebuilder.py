"""Build outline data module for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.core.contentscreator import get_contents_list
from storybuilder.dataconverter import conv_text_list_by_tags
from storybuilder.datatypes import ContentsData, OutlineData, OutputData, StoryData
from storybuilder.datatypes import OutlineRecord, StoryRecord
from storybuilder.formatter import format_contents_table_data, format_outline_data, get_breakline
from storybuilder.util import assertion
from storybuilder.util.log import logger


# Main Function
def on_build_outline(story_data: StoryData, tags: dict) -> OutputData:
    assert isinstance(story_data, StoryData)
    assert isinstance(tags, dict)

    contents = assertion.is_instance(get_contents_list(story_data), ContentsData)
    books = assertion.is_instance(_get_outline_data('book', story_data), OutlineData)
    chapters = assertion.is_instance(_get_outline_data('chapter', story_data), OutlineData)
    episodes = assertion.is_instance(_get_outline_data('episode', story_data), OutlineData)
    scenes = assertion.is_instance(_get_outline_data('scene', story_data), OutlineData)

    outlines = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_outline_data('book', books) \
            + [get_breakline()] \
            + format_outline_data('chapter', chapters) \
            + [get_breakline()] \
            + format_outline_data('episode', episodes) \
            + [get_breakline()] \
            + format_outline_data('scene', scenes)

    output_data = conv_text_list_by_tags(outlines, tags)

    return OutputData(output_data)


# Private Functions
def _get_outline_data(level: str, story_data: StoryData) -> OutlineData:
    assert isinstance(level, str)
    assert isinstance(story_data, StoryData)

    tmp = []
    target = 'outline'

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if level == 'book' and record.category == 'book':
            tmp.append(
                    OutlineRecord(record.data['title'], record.data[target]))
        elif level == 'chapter' and record.category == 'chapter':
            tmp.append(
                    OutlineRecord(record.data['title'], record.data[target]))
        elif level == 'episode' and record.category == 'episode':
            tmp.append(
                    OutlineRecord(record.data['title'], record.data[target]))
        elif level == 'scene' and record.category == 'scene':
            tmp.append(
                    OutlineRecord(record.data['title'], record.data[target]))
        else:
            continue

    return OutlineData(tmp)


