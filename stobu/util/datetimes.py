"""Utility module for date and time controls."""


# Official Libraries
import datetime

# Thirdparty Libraries
from dateutil.relativedelta import relativedelta


# My Modules


__all__ = (
        'get_next_month_day_str',
        )


# Main Functions
def get_next_month_day_str(year: str, mon: str, day: str,
        add_mon: int, add_day: int) -> str:
    assert isinstance(year, str)
    assert isinstance(mon, str)
    assert isinstance(day, str)
    assert isinstance(add_mon, int)
    assert isinstance(add_day, int)

    basedate = datetime.date(int(year), int(mon), int(day))
    elapsed = basedate + relativedelta(months=add_mon, days=add_day)
    return str(elapsed.month) + "/" + str(elapsed.day)
