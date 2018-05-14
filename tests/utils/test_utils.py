from datetime import datetime, timedelta

from pytest import raises

from slimleaf.utils import (
    appendable_datetime,
    add_days,
    current_datetime,
    wait_for_result,
    unique_email,
    mysql_datetime
)


# Test variables
dt = datetime.now()


def test_mysql_dt():
    assert mysql_datetime(dt) == dt.strftime('%Y-%m-%d %H:%M:%S')


def test_appendable_dt():
    assert appendable_datetime(dt, millis=True) == dt.strftime('%Y%m%d%H%M%S%f')


def test_add_days():
    days = -2
    assert add_days(dt, days=days) == (dt + timedelta(days))


def test_unique_email():
    assert isinstance(unique_email(), str)


def test_current_dt():
    assert isinstance(current_datetime(), datetime)


def test_can_wait_for_result():
    def test_func():
        return True

    assert wait_for_result(func=test_func)


def test_wait_for_result_timeout():
    def test_func():
        return False

    with raises(TimeoutError) as timeout_exc:
        wait_for_result(func=test_func, wait_secs=1)
    assert str(timeout_exc.value)
