"""Test for action data creator."""

# Official Libraries
import pytest

# My Modules
from stobu.core.actiondatacreator import ACT_TYPE_TABLE
from stobu.types.action import ActType, NORMAL_ACTIONS


# Test: covered act types
def test_act_type_table():

    for act in NORMAL_ACTIONS:

        assert act in ACT_TYPE_TABLE, f"Missing the ACT in Table!: {act}"
