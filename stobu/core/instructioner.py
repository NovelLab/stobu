"""Instruction module."""

# Official Libraries


# My Modules
from stobu.syss import messages as msg
from stobu.tools.translater import translate_tags_str
from stobu.types.action import ActDataType, ActionRecord, ActionsData, ActType
from stobu.types.action import NORMAL_ACTIONS
from stobu.utils.log import logger


__all__ = (
        'actions_data_apply_instructions',
        )


# Define Constants
PROC = 'INSTRUCTION'


INST_PARAGRAPH_START = ('P', 'pr')

INST_BREAK = ('B', 'BR', 'br')

INST_PARAGRAPH_END = ('PE', 'pend')

INST_ALIAS = ('A', 'alias')

INST_FORESHADOW = ('FS', 'FLAG', 'foreshadow')

INST_PAYOFF = ('PO', 'DISFLAG', 'payoff')


# Main
def actions_data_apply_instructions(actions_data: ActionsData, tags: dict) -> ActionsData:
    assert isinstance(actions_data, ActionsData)
    assert isinstance(tags, dict)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = []
    alias = {}

    # TODO: パラグラフはパラグラフのActDataTypeで制御し、インデントやBRはここでは命令分以外は入れない
    for record in actions_data.get_data():
        assert isinstance(record, ActionRecord)
        if ActDataType.INSTRUCTION is record.subtype:
            if record.subject in INST_PARAGRAPH_START:
                tmp.append(_get_record_as_paragraph_start())
            elif record.subject in INST_PARAGRAPH_END:
                tmp.append(_get_record_as_paragraph_end())
            elif record.subject in INST_BREAK:
                tmp.append(_get_record_as_br())
            elif record.subject in INST_ALIAS:
                short, origin = record.outline.split('=')
                alias[short] = origin
            elif record.subject in INST_FORESHADOW:
                tmp.append(_record_as_foreshadow_from(record, tags))
            elif record.subject in INST_PAYOFF:
                tmp.append(_record_as_payoff_from(record, tags))
            else:
                logger.warning(msg.ERR_FAIL_INVALID_DATA.format(data=f"instruction type in {PROC}"))
                continue
        elif ActDataType.SCENE_START is record.subtype:
            alias = {}
            tmp.append(record)
        elif record.type in NORMAL_ACTIONS:
            tmp.append(_conv_shorter_by_alias(record, alias))
        else:
            tmp.append(record)

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return ActionsData(tmp)


# Private Functions
def _conv_shorter_by_alias(record: ActionRecord, alias: dict) -> ActionRecord:
    assert isinstance(record, ActionRecord)
    assert isinstance(alias, dict)

    subject = record.subject

    if record.subject in alias.keys():
        subject = alias[record.subject]

    return ActionRecord(
            record.type,
            record.subtype,
            subject,
            translate_tags_str(record.outline, alias),
            translate_tags_str(record.desc, alias),
            record.flags,
            translate_tags_str(record.note, alias),
            )


def _get_record_as_br() -> ActionRecord:
    return ActionRecord(ActType.DATA, ActDataType.BR, '\n')


def _get_record_as_paragraph_end() -> ActionRecord:
    return ActionRecord(ActType.DATA, ActDataType.PARAGRAPH_END, '')


def _get_record_as_paragraph_start() -> ActionRecord:
    return ActionRecord(ActType.DATA, ActDataType.PARAGRAPH_START, '')


def _record_as_foreshadow_from(record: ActionRecord, tags: dict) -> ActionRecord:
    assert isinstance(record, ActionRecord)
    assert isinstance(tags, dict)

    subject, flag = '', record.outline

    if ':' in record.outline:
        subject, flag = record.outline.split(':')
        if subject:
            subject = translate_tags_str(subject, tags, True, None)

    return ActionRecord(
            ActType.DATA,
            ActDataType.FORESHADOW,
            subject,
            flag)


def _record_as_payoff_from(record: ActionRecord, tags: dict) -> ActionRecord:
    assert isinstance(record, ActionRecord)
    assert isinstance(tags, dict)

    subject, flag = '', record.outline

    if ':' in record.outline:
        subject, flag = record.outline.split(':')
        if subject:
            subject = translate_tags_str(subject, tags, True, None)

    return ActionRecord(
            ActType.DATA,
            ActDataType.PAYOFF,
            subject,
            flag)
