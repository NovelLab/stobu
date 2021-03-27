"""Utility module for action record."""


# Official Libraries


# My Modules
from stobu.types.actiontypes import ActRecordType


__all__ = (
        )


# Functions
def get_scene_end_action_record() -> ActionRecord:
    """Get Scene-end action record."""
    return ActionRecord(ActRecordType.SCENE_DATA, 'end')


def get_scene_start_action_record() -> ActionRecord:
    """Get Scene-start action record."""
    return ActionRecord(ActRecordType.SCENE_DATA, 'start')


