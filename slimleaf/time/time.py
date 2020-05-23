from datetime import datetime, timedelta


def mysql_datetime(dt):
    """Datetime formatted to be digestible by MySQL"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def appendable_datetime(dt, millis=False):
    """Datetime in a format that can be easily appended to strings, with no punctuation. Useful for
    imposing semi-uniqueness on a string.
    """

    return dt.strftime('%Y%m%d%H%M%S{}'.format('%f' if millis else ''))


def iso_utc_offset_datetime(dt, offset=None, minus=False):
    """Datetime including a dummy offset for publish dates which require this sort of thing.
    - offset: Offset in the format of HH:MM(str)"""
    offset = offset or '00:00'
    operator = '+' if not minus else '-'
    return dt.strftime(f'%Y%m%dT%H%M%S{operator}{offset}')


def add_days(dt, days):
    """Returns a datetime adjusted by n days. Past dates are achieved by passing in a negative days
    value.
    """

    return dt + timedelta(days)