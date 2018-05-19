from unittest.mock import MagicMock, patch

from pytest import raises
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from slimleaf.pages import WebPage
from slimleaf.webdriver.exceptions import PageMismatchException
from slimleaf.webdriver.locator import Locator

TEST_URL = 'http://testurl.maga.rip'
TEST_PATH = '/unimportant'


class MockPage(WebPage):

    path = TEST_PATH

    @property
    def unique_locator(self):
        return Locator(By.CSS_SELECTOR, 'unimportant')


@patch('slimleaf.pages.web.web_page.WebDriverWait')
@patch('slimleaf.pages.page.WebDriverWait')
def test_can_use_base_inherited_class(_mock_wait_page, _mock_wait_web, mock_text, mock_driver):

    # Successful arrival
    _mock_wait_page.return_value.until.return_value = MagicMock()
    test_page = MockPage(TEST_URL, mock_driver).go()

    # Validate Page arrival logic
    _mock_wait_page.return_value.until.side_effect = PageMismatchException(
        'Expected to find element in Page'
    )
    with raises(PageMismatchException) as mismatch_exc:
        test_page = MockPage(TEST_URL, mock_driver).go()
    assert 'Expected to find element' in str(mismatch_exc.value)

    # Validate Timeout logic
    _mock_wait_page.return_value.until.side_effect = TimeoutException
    with raises(PageMismatchException) as mismatch_exc:  # Validates expected exception
        test_page = MockPage(TEST_URL, mock_driver).go()

    # Validate title
    mock_driver.title = mock_text
    assert test_page.title == mock_text

    # Validate URL
    assert test_page.url == f'{TEST_URL}{TEST_PATH}'

    # Validate refresh
    _mock_wait_web.return_value.until.side_effect = None
    test_page.refresh()
    mock_driver.refresh.assert_called_once()

    # Validate Scrolling
    test_page.scroll_to_bottom()
    mock_driver.execute_script.assert_called_once()

    mock_driver.reset_mock()
    test_page.scroll_to_center()
    mock_driver.execute_script.assert_called_once()

    mock_driver.reset_mock()
    test_page.scroll_to_top()
    mock_driver.execute_script.assert_called_once()
