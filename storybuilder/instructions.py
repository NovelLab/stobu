"""Instruction module for storybuilder project."""


# Official Libraries


# My Modules
from storybuilder.datatypes import ActionData, ActionRecord
from storybuilder.util.log import logger


# Main Functions
def apply_instruction_to_action_data(action_data: ActionData,
        is_script_mode: bool=False) -> list:
    assert isinstance(action_data, ActionData)
    assert isinstance(is_script_mode, bool)
    logger.debug("Applying instruction to action data...")

    tmp = []
    is_br_mode = True
    has_first_indent = False
    alias = {}

    for record in action_data.get_data():
        assert isinstance(record, ActionRecord)
        if record.type == 'scene-start':
            is_br_mode = True
            has_first_indent = False
            alias = {}
        elif record.type == 'instruction':
            if record.action == 'P':
                # in Paragraph mode
                is_br_mode = False
            elif record.action == 'E':
                # end Paragraph mode
                is_br_mode = True
                has_first_indent = False
                tmp.append(_get_br_action())
            elif record.action in ('B', 'br', 'BR'):
                # break line
                is_br_mode = True
                tmp.append(_get_br_action())
            elif record.action == 'A':
                # alias
                short, origin = record.outline.split('=')
                alias[short] = origin
            else:
                logger.debug("Unimplement instruction!: %s", record.action)
                continue
        elif record.type in ('action', 'text'):
            # alias
            if record.subject in alias.keys():
                record.subject == alias[record.subject]
            # NOTE: other alias?
            # br refine
            if is_script_mode:
                if record.action in ('talk', 'think'):
                    if not record.outline:
                        continue
            else:
                if record.action in ('talk',):
                    if not record.outline and not record.desc:
                        continue
                else:
                    if not record.desc:
                        continue
            if is_br_mode:
                if not record.action in ('talk',):
                    tmp.append(_get_indent_action())
            elif not is_br_mode:
                if not has_first_indent and record.action == 'talk':
                    has_first_indent = True
                elif not has_first_indent:
                    tmp.append(_get_indent_action())
                    has_first_indent = True
            tmp.append(record)
            if is_br_mode:
                tmp.append(_get_br_action())
        else:
            tmp.append(record)

    logger.debug("...Succeeded apply instructions to action data.")
    return ActionData(tmp)


# Private Functions
def _get_br_action() -> ActionRecord:
    return ActionRecord('br', "")


def _get_indent_action() -> ActionRecord:
    return ActionRecord('indent', "")

