import time
from uuid import uuid1
from datetime import datetime, timedelta


def mysql_datetime(dt):
    """Datetime formatted to be digestible by MySQL"""

    return dt.strftime('%Y-%m-%d %H:%M:%S')


def current_datetime():
    """Current datetime

    When complex date manipulation is required, readable datetimes increase code clarity
    """

    return datetime.now()


def add_days(dt, days):
    """Datetime adjusted by n days. Past dates are achieved by passing in a negative days value."""

    return dt + timedelta(days)


def appendable_datetime(dt, millis=False):
    """Datetime in a format that can be easily appended to strings, with no punctuation.

    Useful for imposing semi-uniqueness on a string.
    """

    return dt.strftime('%Y%m%d%H%M%S{}'.format('%f' if millis else ''))


def normalize_name(name):
    return name.strip().replace(' ', '_').lower()


def unique_email():
    """Generates a unique email address"""
    email = f"unique_email_{uuid1()}@test.com"
    return email


def wait_for_result(
        func, f_args=None, f_kwargs=None, expected_result=True, wait_secs=10, poll_secs=.5):
    """Poll the results of a function until expected outcome is reached or timeout expires"""

    f_args = f_args or []
    f_kwargs = f_kwargs or {}
    start_time = time.time()

    while (time.time() - start_time) < wait_secs:
        result = func(*f_args, **f_kwargs)
        if result == expected_result:
            return result
        time.sleep(poll_secs)
    raise TimeoutError(
        f'Waited {wait_secs} secs for {expected_result}, but last check returned {result}')
