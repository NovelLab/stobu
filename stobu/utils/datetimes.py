"""Utility module for date and time controls."""


# Official Libraries
import datetime

# Thirdparty Libraries
from dateutil.relativedelta import relativedelta


# My Modules


__all__ = (
        'after_day_str_from',
        'next_day_str_from',
        'next_month_str_from',
        )


# Main Functions
def after_day_str_from(year: str, mon: str, day: str,
        aftermon: int, afterday: int) -> str:
    assert isinstance(year, str)
    assert isinstance(mon, str)
    assert isinstance(day, str)
    assert isinstance(aftermon, int)
    assert isinstance(afterday, int)

    basedate = datetime.date(int(year), int(mon), int(day))
    elapsed = basedate + relativedelta(months=aftermon, days=afterday)

    return str(elapsed.month) + '/' + str(elapsed.day)


def next_day_str_from(year: str, mon: str, day: str) -> str:
    return after_day_str_from(year, mon, day, 0, 1)


def next_month_str_from(year: str, mon: str, day: str) -> str:
    return after_day_str_from(year, mon, day, 1, 0)
