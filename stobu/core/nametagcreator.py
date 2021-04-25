"""Create name tag module."""

# Official Libraries


# My Modules
from stobu.elms.books import BookItem
from stobu.elms.events import EventItem
from stobu.elms.items import ItemItem
from stobu.elms.persons import PersonItem
from stobu.elms.stages import StageItem
from stobu.elms.words import WordItem
from stobu.syss import messages as msg
from stobu.tools.datareader import get_person_data, get_mob_data, get_time_data, get_book_data
from stobu.tools.datareader import get_fixture_data, get_term_data
from stobu.tools.filedatareader import read_markdown_data_as_yaml
from stobu.tools.pathgetter import filepaths_by_elm
from stobu.types.element import ElmType
from stobu.utils import assertion
from stobu.utils.dicts import combine_dicts, dict_sorted
from stobu.utils.fileio import read_file
from stobu.utils.filepath import basename_of
from stobu.utils.log import logger
from stobu.utils.strings import hankaku_to_zenkaku


__all__ = (
        'get_calling_tags',
        'get_nametags',
        )


# Define Constants
PROC = 'CREATE NAME TAG'


NAME_ELMS = [
        ElmType.EVENT,
        ElmType.WORD,
        ElmType.ITEM,
        ElmType.STAGE,
        ElmType.PERSON,
        ]


TAG_VALUE_ELMS = {
        ElmType.EVENT: EventItem.NAME,
        ElmType.ITEM: ItemItem.NAME,
        ElmType.PERSON: PersonItem.NAME,
        ElmType.STAGE: StageItem.NAME,
        ElmType.WORD: WordItem.NAME,
        }


TAG_PREFIX_ELMS = {
        ElmType.EVENT: 'e',
        ElmType.ITEM: 'i',
        ElmType.PERSON: 'n',
        ElmType.STAGE: 't',
        ElmType.WORD: 'w',
        }


# Main
def get_calling_tags() -> dict:
    tmp = {}

    persons = filepaths_by_elm(ElmType.PERSON)

    for fname in persons:
        data = get_person_data(fname)
        name = data[str(PersonItem.NAME)]
        calling = data[str(PersonItem.CALLING)]
        calling['S'] = name
        calling['M'] = calling['me'] if 'me' in calling else '私'
        tmp[basename_of(fname)] = calling

    return tmp


def get_nametags() -> dict:
    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = _add_mob_tags()

    tmp = combine_dicts(tmp, _add_time_tags())

    tmp = combine_dicts(tmp, _add_fixture_tags())

    tmp = combine_dicts(tmp, _add_term_tags())

    for elm in NAME_ELMS:
        paths = filepaths_by_elm(elm)
        for path in paths:
            if not _append_tag(tmp, elm, path):
                logger.warning(msg.ERR_FAIL_INVALID_DATA.format(
                    data='appen key or value: {PROC}'))
            if ElmType.PERSON is elm:
                if not _append_person_fullname(tmp, path):
                    logger.warning(msg.ERR_FAIL_INVALID_DATA.format(
                        data='append full name: {PROC}'))

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return dict_sorted(tmp, True)


# Private Functions
def _add_fixture_tags() -> dict:
    data = assertion.is_dict(get_fixture_data())
    tmp = {}
    for key, val in data.items():
        tmp[key] = val['name']
    return tmp


def _add_mob_tags() -> dict:
    mobs = get_book_data()[str(BookItem.MOBS)]
    data = assertion.is_dict(get_mob_data())
    tmp = {}
    for key, val in data.items():
        tmp[key] = val['name']
        for i in range(int(mobs)):
            tmp[key + str(i)] = val['name'] + hankaku_to_zenkaku(str(i))
    return tmp


def _add_term_tags() -> dict:
    data = assertion.is_dict(get_term_data())
    tmp = {}
    for key, val in data.items():
        tmp[key] = val['name']
    return tmp


def _add_time_tags() -> dict:
    data = assertion.is_dict(get_time_data())
    tmp = {}
    for key, val in data.items():
        tmp[key] = val['name']
    return tmp


def _append_key_and_value(data: dict, key: str, value: str) -> bool:
    assert isinstance(data, dict)
    assert isinstance(key, str)
    assert isinstance(value, str)

    data[key] = value

    return True


def _append_tag(data: dict, elm: ElmType, path: str) -> bool:
    assert isinstance(data, dict)
    assert isinstance(elm, ElmType)
    assert isinstance(path, str)

    elm_data = read_markdown_data_as_yaml(read_file(path))
    val = elm_data[str(TAG_VALUE_ELMS[elm])]
    with_prefix = f"{TAG_PREFIX_ELMS[elm]}_{basename_of(path)}"

    return _append_key_and_value(data, basename_of(path), val) \
            or _append_key_and_value(data, with_prefix, val)


def _append_person_fullname(data: dict, path: str) -> bool:
    assert isinstance(data, dict)
    assert isinstance(path, str)

    elm_data = read_markdown_data_as_yaml(read_file(path))
    basetag = basename_of(path)
    name = elm_data[str(PersonItem.NAME)]
    fullname = elm_data[str(PersonItem.FULLNAE)]
    last, first = fullname.split(',') if ',' in fullname else ('', name)

    return _append_key_and_value(data, f"fn_{basetag}", first) \
            and _append_key_and_value(data, f"ln_{basetag}", last) \
            and _append_key_and_value(data, f"full_{basetag}", f"{last}{first}") \
            and _append_key_and_value(data, f"efull_{basetag}", f"{first}・{last}")
