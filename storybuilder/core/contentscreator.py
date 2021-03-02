"""Story contents create module."""


# Official Libraries


# My Modules
from storybuilder.datatypes import ContentRecord, StoryRecord
from storybuilder.datatypes import ContentsData, StoryData
from storybuilder.util.log import logger


__all__ = (
        'get_contents_list',
        )


# Main Function
def get_contents_list(story_data: StoryData) -> ContentsData:
    assert isinstance(story_data, StoryData)

    tmp = []
    bk_idx, ch_idx, ep_idx, sc_idx = 1, 1, 1, 1

    for record in story_data.get_data():
        assert isinstance(record, StoryRecord)
        if record.category == 'book':
            tmp.append(ContentRecord('book', record.data['title'], bk_idx))
            bk_idx += 1
        elif record.category == 'chapter':
            tmp.append(ContentRecord('chapter', record.data['title'], ch_idx))
            ch_idx += 1
        elif record.category == 'episode':
            tmp.append(ContentRecord('episode', record.data['title'], ep_idx))
            ep_idx += 1
        elif record.category == 'scene':
            tmp.append(ContentRecord('scene', record.data['title'], sc_idx))
            sc_idx += 1
        else:
            logger.error("Invalid StoryRecord data!: %s", record)

    return ContentsData(tmp)


