"""Utilities for working with dates."""

import calendar
import datetime
import itertools


MONTHS = dict((name.lower(), i) for i, name in itertools.chain(
    enumerate(calendar.month_abbr[1:], start=1),
    enumerate(calendar.month_name[1:], start=1),
    enumerate(['{0:1d}'.format(i) for i in range(1, 13)], start=1),
    enumerate(['{0:02d}'.format(i) for i in range(1, 13)], start=1)))


def month_number(month):
    """Turns a month name into its corresponding month number.

    It recognizes full and abbreviated (three letters) English month names
    (case insensitive) as well as month number with or without a leading 0.

    Args:
      month: A string; the name of a month.
    Returns:
      An int, the number in [1,12] corresponding to the given month name,
      or None if it does not recognize the given name.
    """
    return MONTHS.get(month.lower()) if isinstance(month, str) else None


def add_biz_days(date, num_biz_days):
    """Add a number of business days to a date.

    If the starting date falls on a weekend, it is moved to the next business
    day before adding the delta.

    Args:
      date: The starting date; a datetime.date object.
      num_biz_days: The number of business days to add to the starting date;
        a non-negative int.
    Returns:
      A datetime.date object.
    """
    assert num_biz_days >= 0, 'Invalid num_biz_days value ({}): must be non-negative'.format(num_biz_days)

    # Break the delta into a number of full weeks and a remainder
    num_weeks, num_biz_days_left = divmod(num_biz_days, 5)
    num_days = num_weeks * 7 + num_biz_days_left
    weekday = date.weekday()    # Monday is weekday 0
    # If the starting date falls on a weekend, move it to the next business day
    if weekday >= 5:
        num_days += 7 - weekday
        weekday = 0
    # If the number of business days left in the delta spans a weekend, add
    # that in a well
    if weekday + num_biz_days_left >= 5:
        num_days += 2
    return date + datetime.timedelta(days=num_days)
