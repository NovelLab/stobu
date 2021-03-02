"""Count module for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.datatypes import CountRecord
from storybuilder.util.log import logger



# Main Functions
def get_charcounts_script_data(formatted: list) -> list:
    assert isinstance(formatted, list)

    tmp = []

    books = ["",]
    chapters = ["",]
    episodes = ["",]
    scenes = ["",]
    book_titles = ["",]
    ch_titles = ["",]
    ep_titles = ["",]
    sc_titles = ["",]
    book_idx, ch_idx, ep_idx, sc_idx = 0, 0, 0, 0

    for line in formatted:
        assert isinstance(line, str)
        if line.startswith('# '):
            # Book title
            book_idx += 1
            books.append("")
            book_titles.append(line[2:].rstrip('\n\r'))
        elif line.startswith('## '):
            # Chapter title
            ch_idx += 1
            chapters.append("")
            ch_titles.append(line[3:].rstrip('\n\r'))
        elif line.startswith('### '):
            # Episode title
            ep_idx += 1
            episodes.append("")
            ep_titles.append(line[4:].rstrip('\n\r'))
        elif line.startswith('**'):
            # Scene title
            sc_idx += 1
            scenes.append("")
            sc_titles.append(line.replace('**', '').rstrip('\n\r'))
        elif line.startswith('○　'):
            # Spin
            pass
        else:
            # Text
            books[book_idx] += line
            chapters[ch_idx] += line
            episodes[ep_idx] += line
            scenes[sc_idx] += line

    book_idx = 1
    tmp.append(CountRecord('book', '_head', 0))
    for book, title in zip(books[1:], book_titles[1:]):
        tmp.append(CountRecord('book', title, len(books[book_idx])))
        book_idx += 1
    tmp.append(CountRecord('book', '_end', 0))

    ch_idx = 1
    tmp.append(CountRecord('chapter', '_head', 0))
    for chapter, title in zip(chapters[1:], ch_titles[1:]):
        tmp.append(CountRecord('chapter', title, len(chapters[ch_idx])))
        ch_idx += 1
    tmp.append(CountRecord('chapter', '_end', 0))

    ep_idx = 1
    tmp.append(CountRecord('episode', '_head', 0))
    for episode, title in zip(episodes[1:], ep_titles[1:]):
        tmp.append(CountRecord('episode', title, len(episodes[ep_idx])))
        ep_idx += 1
    tmp.append(CountRecord('episode', '_end', 0))

    sc_idx = 1
    tmp.append(CountRecord('scene', '_head', 0))
    for scene, title in zip(scenes[1:], sc_titles[1:]):
        tmp.append(CountRecord('scene', title, len(scenes[sc_idx])))
        sc_idx += 1
    tmp.append(CountRecord('scene', '_end', 0))

    return tmp

