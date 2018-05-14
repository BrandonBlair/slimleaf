from datetime import datetime
import time

from slimleaf.exceptions import SlimleafException


def wait_through_exception_then_return(
    exc, func, func_args=None, func_kwargs=None, timeout_secs=5, poll_secs=.5):  # noqa
    """Waits for a function to stop raising an exception, then returns the value if successful."""

    start_time = datetime.now()
    curr_time = datetime.now()

    func_args = func_args or []
    func_kwargs = func_kwargs or {}

    while (curr_time - start_time).total_seconds() < timeout_secs:
        try:
            result = func(*func_args, **func_kwargs)
            return result
        except exc as wde:
            time.sleep(poll_secs)
            curr_time = datetime.now()
    raise SlimleafException(f'Exception {exc} did not subside as expected')
