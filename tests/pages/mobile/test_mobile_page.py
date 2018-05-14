from unittest.mock import MagicMock, patch

from pytest import raises
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from slimleaf.pages import MobilePage
from slimleaf.exceptions import SlimleafException
from slimleaf.webdriver.exceptions import PageMismatchException
from slimleaf.webdriver.locator import Locator


class MockPage(MobilePage):
    @property
    def unique_locator(self):
        return MagicMock()


@patch('slimleaf.pages.page.WebDriverWait')
def test_can_use_base_inherited_class(_mock_wait, mock_mobile_driver):
    mock_elem = MagicMock()
    _mock_wait.return_value.until.return_value = mock_elem

    MockPage(mock_mobile_driver)
    _mock_wait.return_value.until.assert_called_once()

    # Validate Page arrival logic
    exc_msg = 'Expected to find element'
    _mock_wait.return_value.until.side_effect = PageMismatchException(
        'Expected to find element in Page'
    )
    with raises(PageMismatchException) as mismatch_exc:
        MockPage(mock_mobile_driver)
    assert exc_msg in str(mismatch_exc.value)

    # Validate Timeout logic
    _mock_wait.return_value.until.side_effect = TimeoutException
    with raises(PageMismatchException) as mismatch_exc:
        MockPage(mock_mobile_driver)
    assert exc_msg in str(mismatch_exc.value)


def test_can_access_page_html_tree(mock_mobile_driver):
    fake_elem = MagicMock()
    fake_elem.etree_locator = Locator(by=By.ID, value='unimportant')

    fake_paragraph_txt = 'This is a paragraph'
    fake_source_1 = f"<html><body><p>{fake_paragraph_txt}</p></body></html>"
    mock_mobile_driver.page_source = fake_source_1

    page = MockPage(mock_mobile_driver)
    assert page.html_tree.tag == 'html'

    # Unsupported By
    with raises(SlimleafException) as bad_by_exc:
        page.get_element_tree(fake_elem)
    assert 'not supported' in str(bad_by_exc.value)

    # Too many matches
    fake_elem.etree_locator = Locator(by=By.CSS_SELECTOR, value='p')
    fake_source_2 = f"<html><body><p>{fake_paragraph_txt}</p><p>unimportant</p></body></html>"
    mock_mobile_driver.page_source = fake_source_2
    with raises(SlimleafException) as too_many_results_exc:
        page.get_element_tree(fake_elem)
    assert 'Expected one' in str(too_many_results_exc.value)

    # No matches
    fake_elem.etree_locator = Locator(by=By.CSS_SELECTOR, value='a')
    with raises(SlimleafException) as no_results_exc:
        page.get_element_tree(fake_elem)
    assert 'No matching tree object' in str(no_results_exc.value)

    # Successful Tree generation
    mock_mobile_driver.page_source = fake_source_1  # Only one <p> tag
    fake_elem.etree_locator = Locator(by=By.CSS_SELECTOR, value='p')
    assert page.get_element_tree(fake_elem).text == fake_paragraph_txt
