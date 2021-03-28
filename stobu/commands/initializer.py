"""Init module for stobu project."""

# Official Libraries


# My Modules
from stobu.systems import messages as msg
from stobu.tools import filechecker as checker
from stobu.tools import pathmanager as ppath
from stobu.util.log import logger


__all__ = (
        'init_project',
        )

# Define Constants
PROC = 'Init Project'


# Main Functions
def init_project() -> bool:
    logger.debug(msg.MSG_START_PROC.format(proc=PROC))

    '''
    if not check_and_create_defaults(creator):
        logger.error("Failed check and create defaults!")
        return False
    '''

    if not pre_process():
        return False

    if not main_process():
        return False

    if not post_process():
        return False

    logger.debug(msg.MSG_FINISH_PROC.format(proc=PROC))
    return True


# Process Functions
def pre_process() -> bool:
    _PROC = f"Pre Process in {PROC}"
    logger.debug(msg.MSG_START_PROC.format(proc=_PROC))

    if not _check_and_create_the_file_using_template(
            'project', ppath.get_project_path(),
            checker.exists_project_file, creator.get_project_template):
        logger.debug("Failure creating the project file!")
        return False

    logger.debug(msg.MSG_FINISH_PROC.format(proc=_PROC))
    return True


def main_process() -> bool:
    _PROC = f"Main Process in {PROC}"
    logger.debug(msg.MSG_START_PROC.format(proc=_PROC))
    logger.debug(msg.MSG_FINISH_PROC.format(proc=_PROC))
    return True


def post_process() -> bool:
    _PROC = f"Post Process in {PROC}"
    logger.debug(msg.MSG_START_PROC.format(proc=_PROC))
    logger.debug(msg.MSG_FINISH_PROC.format(proc=_PROC))
    return True


# Private Functions
def _check_and_create_the_file_using_template(target: str, path: str,
        check_method: Callable, create_method: Callable) -> bool:
    assert isinstance(target, str)
    assert isinstance(path, str)
    assert callable(check_method)
    assert callable(create_method)
    logger.debug(START_PROCESS_CREATE_FILE.format(target=target))

    if check_method():
        logger.debug(ERR_ALREADY_EXISTS.format(target=f"{target} file"), path)
        return True

    template_data = create_method()
    if not template_data:
        logger.error(ERR_MISSING_TEMPLATE_DATA.format(target=target), template_data)
        return False

    if not write_file(path, template_data):
        logger.error(ERR_CREATE_FILE.format(target=target), path)
        return False

    logger.debug(FINISH_PROCESS_CREATE_FILE.format(target=target))
    return True



