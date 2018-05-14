from unittest.mock import MagicMock

from pytest import raises

from slimleaf.webdriver.custom_waits import wait_through_exception_then_return
from slimleaf.exceptions import SlimleafException


def test_can_wait_through_exception(mock_text):
    mock_func = MagicMock(side_effect=[TimeoutError, mock_text])
    result = wait_through_exception_then_return(exc=TimeoutError, func=mock_func)
    assert result == mock_text

    mock_func = MagicMock(side_effect=TimeoutError)
    with raises(SlimleafException) as timeout_exc:
        wait_through_exception_then_return(exc=TimeoutError, func=mock_func)
    assert 'did not subside' in str(timeout_exc.value)
