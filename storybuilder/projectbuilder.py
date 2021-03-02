"""Building module for storybuilder project."""


# Official Libraries
import argparse
import os


# My Modules
from storybuilder.dataconverter import conv_action_record_from_scene_action, conv_text_from_tag, conv_to_story_record, conv_code_from_action_record
from storybuilder.datatypes import StoryRecord, OutlineRecord, ContentRecord, PlotRecord, ActionRecord, StoryCode
from storybuilder.datatypes import CountRecord
from storybuilder.formatter import format_contents_table_data, format_outline_data, format_plot_data, format_script_data, format_novel_data
from storybuilder.formatter import format_charcounts_outline, format_charcounts_plot, format_charcounts_script
from storybuilder.formatter import get_breakline
from storybuilder.instructions import apply_instruction_to_action_data
from storybuilder.nametagmanager import NameTagDB
from storybuilder.projectcounter import get_charcounts_script_data
import storybuilder.projectpathmanager as ppath
from storybuilder.util import assertion
from storybuilder.util.fileio import read_file_as_yaml, read_file_as_markdown, write_file
from storybuilder.util.filepath import basename_of
from storybuilder.util.log import logger


__all__ = (
        'switch_command_to_build',
        )


# Main Functions
def switch_command_to_build(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('b', 'build')

    # create tag db
    tagdb = get_nametag_db()

    # get story data
    story_data = get_story_data()

    # - outline
    if cmdargs.outline:
        logger.debug("Building outline data...")
        outline_data = build_outline(story_data, tagdb)
        if outline_data:
            path = os.path.join(ppath.get_build_dir_path(), "outline.md")
            if not write_file(path, "".join(outline_data)):
                logger.error("...Failed to write the output outline data!")
                return False
            else:
                logger.debug("...Succeeded to output the outline data.")
        else:
            logger.error("...Failed to build the output data in outline process!: %s", outline_data)
            return False

    # - plot
    if cmdargs.plot:
        logger.debug("Building plot data...")
        plot_data = build_plot(story_data, tagdb)
        if plot_data:
            path = os.path.join(ppath.get_build_dir_path(), "plot.md")
            if not write_file(path, "".join(plot_data)):
                logger.error("...Failed to write the output plot data!")
                return False
            else:
                logger.debug("...Succeeded to output the plot data.")
        else:
            logger.error("...Failed to build the output data in plot process!: %s", plot_data)
            return False

    # - script
    if cmdargs.script:
        logger.debug("Building script data...")
        script_data = build_script(story_data, tagdb)
        if script_data:
            path = os.path.join(ppath.get_build_dir_path(), "script.md")
            if not write_file(path, "".join(script_data)):
                logger.error("...Failed to write the output script data!")
                return False
            else:
                logger.debug("...Succeeded to output the script data.")
        else:
            logger.error("...Failed to build the output data in script process!: %s", script_data)
            return False

    # - novel
    if cmdargs.novel:
        logger.debug("Building novel data...")
        novel_data = build_novel(story_data, tagdb)
        if novel_data:
            path = os.path.join(ppath.get_build_dir_path(), "novel.md")
            if not write_file(path, "".join(novel_data)):
                logger.error("...Failed to write the output novel data!")
                return False
            else:
                logger.debug("...Succeeded to output the novel data.")
        else:
            logger.error("...Failed to build the output data in novel process!: %s", novel_data)
            return False

    # - base data
    base_data = build_basedata(cmdargs, story_data, tagdb)
    if base_data:
        path = os.path.join(ppath.get_build_dir_path(), "data.md")
        if not write_file(path, "".join(base_data)):
            logger.error("...Failed to write the output base data!")
            return False
        else:
            logger.debug("...Succeeded to output the base data.")
    else:
        logger.error("...Failed to build the output data in base data process!: %s", base_data)
        return False

    return True


## Build Functions
def build_basedata(cmdargs: argparse.Namespace, story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    tmp = []

    if cmdargs.outline:
        # outline data
        tmp.extend(get_basedata_outline_charcounts(story_data, tags))
    if cmdargs.plot:
        # plot data
        tmp.extend(get_basedata_plot_charcounts(story_data, tags))
    if cmdargs.script:
        # script data
        tmp.extend(get_basedata_script_charcounts(story_data, tags))
    if cmdargs.novel:
        # novel data
        pass

    contents = _get_contents_list(story_data)

    basedata = format_contents_table_data(contents) \
            + ['\n', get_breakline()] \
            + tmp

    output_data = _convert_list_from_tag(basedata, tags)

    return output_data


def build_novel(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    tmp = []

    action_data = _get_action_data(story_data)

    action_data_applied = apply_instruction_to_action_data(action_data)

    action_data_tagfixed = _convert_list_from_tag_in_action_data(
            action_data_applied, _get_calling_tags())

    story_code_data = _get_story_code_data(action_data_tagfixed, False)

    contents = _get_contents_list(story_data)

    novels = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_novel_data(story_code_data)

    output_data = _convert_list_from_tag(novels, tags)

    return output_data


def build_outline(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    contents = _get_contents_list(story_data)
    books = _get_outline_data('book', story_data)
    chapters = _get_outline_data('chapter', story_data)
    episodes = _get_outline_data('episode', story_data)
    scenes = _get_outline_data('scene', story_data)

    outlines = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_outline_data('book', books) \
            + [get_breakline()] \
            + format_outline_data('chapter', chapters) \
            + [get_breakline()] \
            + format_outline_data('episode', episodes) \
            + [get_breakline()] \
            + format_outline_data('scene', scenes)

    output_data = _convert_list_from_tag(outlines, tags)

    return output_data


def build_plot(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    contents = _get_contents_list(story_data)
    books = _get_plot_data('book', story_data)
    chapters = _get_plot_data('chapter', story_data)
    episodes = _get_plot_data('episode', story_data)
    scenes = _get_plot_data('scene', story_data)

    plots = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_plot_data('book', books) \
            + [get_breakline()] \
            + format_plot_data('chapter', chapters) \
            + [get_breakline()] \
            + format_plot_data('episode', episodes) \
            + [get_breakline()] \
            + format_plot_data('scene', scenes)

    output_data = _convert_list_from_tag(plots, tags)

    return output_data


def build_script(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    tmp = []

    action_data = _get_action_data(story_data)

    action_data_applied = apply_instruction_to_action_data(action_data, True)

    action_data_tagfixed = _convert_list_from_tag_in_action_data(
            action_data_applied, _get_calling_tags())

    story_code_data = _get_story_code_data(action_data_tagfixed, True)

    contents = _get_contents_list(story_data)

    scripts = format_contents_table_data(contents) \
            + ["\n", get_breakline()] \
            + format_script_data(story_code_data, tags)

    output_data = _convert_list_from_tag(scripts, tags)

    return output_data


# Functions
def get_basedata_outline_charcounts(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    outlines = _get_outline_char_counts('book', story_data, tags) \
            + _get_outline_char_counts('chapter', story_data, tags) \
            + _get_outline_char_counts('episode', story_data, tags) \
            + _get_outline_char_counts('scene', story_data, tags)

    output_data = format_charcounts_outline(outlines)

    return output_data


def get_basedata_plot_charcounts(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    plots = _get_plot_char_counts('book', story_data, tags) \
            + _get_plot_char_counts('chapter', story_data, tags) \
            + _get_plot_char_counts('episode', story_data, tags) \
            + _get_plot_char_counts('scene', story_data, tags)

    output_data = format_charcounts_plot(plots)

    return output_data


def get_basedata_script_charcounts(story_data: list, tags: dict) -> list:
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    tmp = []

    action_data = _get_action_data(story_data)

    action_data_applied = apply_instruction_to_action_data(action_data, True)

    action_data_tagfixed = _convert_list_from_tag_in_action_data(
            action_data_applied, _get_calling_tags())

    story_code_data = _get_story_code_data(action_data_tagfixed, True)

    formatted = format_script_data(story_code_data, tags)

    scriptcounts = get_charcounts_script_data(formatted)

    output_data = format_charcounts_script(scriptcounts)
    return output_data


def get_nametag_db() -> dict:
    logger.debug("Creating Name tag DB...")
    db = NameTagDB()

    logger.debug("> word names to DB")
    if not _create_nametags_from_word_files(db):
        return {}

    logger.debug("> item names to DB")
    if not _create_nametags_from_item_files(db):
        return {}

    logger.debug("> stage names to DB")
    if not _create_nametags_from_stage_files(db):
        return {}

    logger.debug("> person names to DB")
    if not _create_nametags_from_person_files(db):
        return {}

    if not db.sort_db():
        logger.error("Failed to sort DB!")
        return {}

    logger.debug("...Succeeded create name tag DB.")
    return db.tags


def get_story_data() -> list:
    order_data = assertion.is_dict(read_file_as_yaml(ppath.get_order_path()))

    serialized = assertion.is_list(_serialized_file_names_from_order(order_data))

    story_data = assertion.is_list(_get_story_data(serialized))

    return story_data


# Private Functions
def _convert_list_from_tag(texts: list, tags: dict) -> list:
    assert isinstance(texts, list)
    assert isinstance(tags, dict)

    tmp = []

    for text in texts:
        tmp.append(conv_text_from_tag(text, tags))
    return tmp


def _convert_list_from_tag_in_action_data(action_data: list, callings: dict,
        prefix: str='$') -> list:
    assert isinstance(action_data, list)
    assert isinstance(callings, dict)
    assert isinstance(prefix, str)

    tmp = []

    for record in action_data:
        assert isinstance(record, ActionRecord)
        if record.type == 'action':
            if record.subject in callings:
                calling = callings[record.subject]
                calling['S'] = f"{record.subject}"
                calling['M'] = calling['me'] if 'me' in calling else '私'
                tmp.append(ActionRecord(
                    record.type,
                    record.subject,
                    record.action,
                    conv_text_from_tag(record.outline, calling, prefix),
                    conv_text_from_tag(record.desc, calling, prefix),
                    record.flags,
                    conv_text_from_tag(record.note, calling, prefix),
                    ))
            else:
                tmp.append(record)
        else:
            tmp.append(record)
    return tmp


def _create_nametags_from_item_files(db: NameTagDB) -> bool:
    items = ppath.get_item_file_paths()
    for fname in assertion.is_list(items):
        data = assertion.is_dict(read_file_as_yaml(fname))
        if not db.add_item(basename_of(fname), data['name']):
            logger.error("Failed to add an item name to tag DB!")
            return False
    return True


def _create_nametags_from_person_files(db: NameTagDB) -> bool:
    persons = ppath.get_person_file_paths()
    for fname in assertion.is_list(persons):
        data = assertion.is_dict(read_file_as_yaml(fname))
        if not db.add_person(basename_of(fname), data['name'], data['fullname']):
            logger.error("Failed to add a person name to tag DB!")
            return False
    return True


def _create_nametags_from_stage_files(db: NameTagDB) -> bool:
    stages = ppath.get_stage_file_paths()
    for fname in assertion.is_list(stages):
        data = assertion.is_dict(read_file_as_yaml(fname))
        if not db.add_stage(basename_of(fname), data['name']):
            logger.error("Failed to add a stage name to tag DB!")
            return False
    return True


def _create_nametags_from_word_files(db: NameTagDB) -> bool:
    words = ppath.get_word_file_paths()
    for fname in assertion.is_list(words):
        data = assertion.is_dict(read_file_as_yaml(fname))
        if not db.add_word(basename_of(fname), data['name']):
            logger.error("Failed to add a word name to tag DB!")
            return False
    return True


def _get_action_data(story_data: list) -> list:
    assert isinstance(story_data, list)
    tmp = []

    for record in story_data:
        assert isinstance(record, StoryRecord)
        if record.category == 'book':
            tmp.append(ActionRecord('book-title', "", "", record.data['title']))
        elif record.category == 'chapter':
            tmp.append(ActionRecord('chapter-title', "", "", record.data['title']))
        elif record.category == 'episode':
            tmp.append(ActionRecord('episode-title', "", "", record.data['title']))
        elif record.category == 'scene':
            ret = _get_action_data_in_scene(record)
            if ret:
                tmp.extend(ret)
        else:
            logger.debug("Unknown StoryRecord data!: %s", record)
            continue
    return tmp


def _get_action_data_in_scene(record: StoryRecord) -> list:
    assert isinstance(record, StoryRecord)
    assert record.category == 'scene'

    tmp = []

    tmp.append(ActionRecord('scene-title', "", "", record.data['title']))
    tmp.append(ActionRecord('scene-camera', record.data['camera'], ""))
    tmp.append(ActionRecord('scene-stage', record.data['stage']))
    tmp.append(ActionRecord('scene-year', record.data['year']))
    tmp.append(ActionRecord('scene-date', record.data['date']))
    tmp.append(ActionRecord('scene-time', record.data['time']))
    tmp.append(ActionRecord('scene-start', ""))

    for line in record.data['markdown']:
        assert isinstance(line, str)
        ret = conv_action_record_from_scene_action(line)
        if ret:
            assert isinstance(ret, ActionRecord)
            tmp.append(ret)

    tmp.append(ActionRecord('scene-end', ""))

    return tmp


def _get_calling_tags() -> dict:
    tmp = {}
    persons = ppath.get_person_file_paths()

    for fname in persons:
        data = read_file_as_yaml(fname)
        tmp[basename_of(fname)] = data['calling']
    return tmp


def _get_contents_list(story_data: list) -> list:
    assert isinstance(story_data, list)

    tmp = []
    bk_idx, ch_idx, ep_idx, sc_idx = 1, 1, 1, 1

    for record in story_data:
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


def _get_outline_char_counts(level: str, story_data: list, tags: dict) -> list:
    assert isinstance(level, str)
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    outline_data = _get_outline_data(level, story_data)
    tmp = []

    for record in outline_data:
        assert isinstance(record, OutlineRecord)
        text = conv_text_from_tag(record.data, tags)
        tmp.append(CountRecord(level, record.title, len(text)))
    totalcount = CountRecord(level, "_head", sum([r.total for r in tmp]))
    return [totalcount] + tmp + [CountRecord(level, "_end", 0)]


def _get_outline_data(level: str, story_data: list) -> list:
    assert isinstance(level, str)
    assert isinstance(story_data, list)

    tmp = []
    target = 'outline'

    for record in story_data:
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

    return tmp


def _get_plot_char_counts(level: str, story_data: list, tags: dict) -> list:
    assert isinstance(level, str)
    assert isinstance(story_data, list)
    assert isinstance(tags, dict)

    plot_data = _get_plot_data(level, story_data)
    tmp = []
    for record in plot_data:
        assert isinstance(record, PlotRecord)
        text = record.setup + record.tp1st + record.develop + record.tp2nd + record.climax + record.resolve
        text_fixed = conv_text_from_tag(text, tags)
        tmp.append(CountRecord(level, record.title, len(text_fixed)))
    totalcount = CountRecord(level, "_head", sum([r.total for r in tmp]))
    return [totalcount] + tmp + [CountRecord(level, "_end", 0)]


def _get_plot_data(level: str, story_data: list) -> list:
    assert isinstance(level, str)
    assert isinstance(story_data, list)

    tmp = []

    for record in story_data:
        assert isinstance(record, StoryRecord)
        if level == record.category:
            plot = record.data['plot']
            tmp.append(
                    PlotRecord(record.data['title'],
                        plot['setup'],
                        plot['tp1st'],
                        plot['develop'],
                        plot['tp2nd'],
                        plot['climax'],
                        plot['resolve']))
        else:
            continue

    return tmp


def _get_story_code_data(action_data: list, is_script_mode: bool) -> list:
    assert isinstance(action_data, list)
    assert isinstance(is_script_mode, bool)

    tmp = []
    for record in action_data:
        assert isinstance(record, ActionRecord)
        ret = conv_code_from_action_record(record, is_script_mode)
        if ret:
            tmp.append(ret)
    return tmp


def _get_story_data(serialized: list) -> list:
    tmp = []

    tmp.append(conv_to_story_record('book/book', read_file_as_yaml(ppath.get_book_path())))

    for fname in serialized:
        tmp.append(conv_to_story_record(
            fname,
            _get_data_from_ordername(fname)))
    return tmp


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

