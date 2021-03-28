"""Command process module for adding."""

# Official Libraries


# My Modules
from stobu.systems import messages as msg
from stobu.tools import commandlineparser as parse
from stobu.util.log import logger


__all__ = (
        'switch_command_to_add',
        )

# Define Constants
PROC = 'add command'

PROC_TARGET = 'add to {target}'


# Main Function
def switch_command_to_add(cmdargs: argparse.Namespace) -> bool:
    assert parse.is_add_command(cmdargs.cmd)
    logger.debug(msg.MSG_START_PROC.format(proc=PROC))

    is_succeeded = False

    if parse.is_arg_chapter(cmdargs.arg0):
        is_succeeded = add_new_chapter(cmdargs.arg1)
    elif parse.is_arg_episode(cmdargs.arg0):
        is_succeeded = add_new_episode(cmdargs.arg1)
    elif parse.is_arg_scene(cmdargs.arg0):
        is_succeeded = add_new_scene(cmdargs.arg1)
    elif parse.is_arg_note(cmdargs.arg0):
        is_succeeded = add_new_note(cmdargs.arg1)
    elif parse.is_arg_person(cmdargs.arg0):
        is_succeeded = add_new_person(cmdargs.arg1)
    elif parse.is_arg_stage(cmdargs.arg0):
        is_succeeded = add_new_stage(cmdargs.arg1)
    elif parse.is_arg_item(cmdargs.arg0):
        is_succeeded = add_new_item(cmdargs.arg1)
    elif parse.is_arg_word(cmdargs.arg0):
        is_succeeded = add_new_word(cmdargs.arg1)
    elif parse.is_arg_todo(cmdargs.arg0):
        is_succeeded = todom.add_todo(cmdargs.arg1)
    elif parse.is_arg_plan(cmdargs.arg0):
        is_succeeded = add_new_plan(cmdargs.arg1)
    elif parse.is_arg_outline(cmdargs.arg0):
        is_succeeded = add_new_outline(cmdargs.arg1)
    elif parse.is_arg_event(cmdargs.arg0):
        is_succeeded = add_new_event(cmdargs.arg1)
    else:
        logger.error(msg.ERR_UNKNOWN_PROC_WITH_DATA.format(proc=PROC), cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error(msg.ERR_FAILURE_PROC.format(proc=PROC))
        return False

    logger.debug(msg.MSG_SUCCESS_PROC.format(proc=PROC))
    return True


# Functions
def add_new_chapter(fname: str) -> bool:
    return _add_new_file('chapter', fname, checker.is_exists_the_chapter,
            ppath.get_chapter_path,
            TemplateCreator.get_instance().get_chapter_template,
            edit_the_chapter)


def add_new_episode(fname: str) -> bool:
    return _add_new_file('episode', fname, checker.is_exists_the_episode,
            ppath.get_episode_path,
            TemplateCreator.get_instance().get_episode_template,
            edit_the_episode)


def add_new_event(fname: str) -> bool:
    return _add_new_file('event', fname, checker.is_exists_the_event,
            ppath.get_event_path,
            TemplateCreator.get_instance().get_event_template,
            edit_the_event)


def add_new_item(fname: str) -> bool:
    return _add_new_file('item', fname, checker.is_exists_the_item,
            ppath.get_item_path,
            TemplateCreator.get_instance().get_item_template,
            edit_the_item)


def add_new_note(fname: str) -> bool:
    return _add_new_file('note', fname, checker.is_exists_the_note,
            ppath.get_note_path,
            TemplateCreator.get_instance().get_note_template,
            edit_the_note)


def add_new_outline(fname: str) -> bool:
    return _add_new_file('outline', fname, checker.is_exists_the_outline,
            ppath.get_outline_path,
            TemplateCreator.get_instance().get_outline_template,
            edit_the_outline)


def add_new_person(fname: str) -> bool:
    return _add_new_file('person', fname, checker.is_exists_the_person,
            ppath.get_person_path,
            TemplateCreator.get_instance().get_person_template,
            edit_the_person)


def add_new_plan(fname: str) -> bool:
    return _add_new_file('plan', fname, checker.is_exists_the_plan,
            ppath.get_plan_path,
            TemplateCreator.get_instance().get_plan_template,
            edit_the_plan)


def add_new_scene(fname: str) -> bool:
    return _add_new_file('scene', fname, checker.is_exists_the_scene,
            ppath.get_scene_path,
            TemplateCreator.get_instance().get_scene_template,
            edit_the_scene)


def add_new_stage(fname: str) -> bool:
    return _add_new_file('stage', fname, checker.is_exists_the_stage,
            ppath.get_stage_path,
            TemplateCreator.get_instance().get_stage_template,
            edit_the_stage)


def add_new_word(fname: str) -> bool:
    return _add_new_file('word', fname, checker.is_exists_the_word,
            ppath.get_word_path,
            TemplateCreator.get_instance().get_word_template,
            edit_the_word)


# Private Functions
def _add_new_file(title: str, fname: str, check_method: Callable,
        path_method: Callable, gettemp_method: Callable, edit_method) -> bool:
    assert isinstance(title, str)
    assert isinstance(fname, str) if fname else True
    assert callable(check_method)
    assert callable(path_method)
    assert callable(gettemp_method)
    assert callable(edit_method)
    logger.debug(msg.MSG_START_PROC.format(proc=PROC_TARGET.format(target=title)))

    _fname = _get_new_filename(fname, f"new {title}")

    if checker.is_invalid_filename(_fname):
        logger.error(msg.ERR_INVALID_FILENAME, _fname)
        return False

    if check_method(_fname):
        logger.error(msg.ERR_DUPLICATED_FILE, _fname)
        return False

    template_data = gettemp_method()
    if not write_file(path_method(_fname), template_data):
        logger.error(msg.ERR_CANNOT_CREATE_FILE, _fname)
        return False

    logger.debug(msg.MSG_FINISH_PROC.format(proc=PROC_TARGET.format(target=title)))

    return edit_method(_fname)


def _get_new_filename(fname: str, msg: str) -> str:
    assert isinstance(msg, str)

    return assertion.is_str(fname) if fname else get_input_filename(
            INPUT_TARGET_FILENAME_MESSAGE.format(target=msg))
