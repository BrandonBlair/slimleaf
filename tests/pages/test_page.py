from unittest.mock import MagicMock

from pytest import raises
from selenium.webdriver.common.by import By

from slimleaf.pages import Page
from slimleaf.exceptions import SlimleafException
from slimleaf.webdriver.locator import Locator

TEST_URL = 'http://testurl.maga.rip'
TEST_PATH = '/unimportant'


class MockPage(Page):

    path = TEST_PATH

    @property
    def unique_locator(self):
        return Locator(By.CSS_SELECTOR, 'unimportant')


def test_can_access_page_html_tree(mock_driver):
    fake_elem = MagicMock()
    fake_elem.etree_locator = Locator(by=By.ID, value='unimportant')

    fake_paragraph_txt = 'This is a paragraph'
    fake_source_1 = f"<html><body><p>{fake_paragraph_txt}</p></body></html>"
    mock_driver.page_source = fake_source_1

    page = MockPage(mock_driver)
    assert page.html_tree.tag == 'html'

    # Unsupported By
    with raises(SlimleafException) as bad_by_exc:
        page.get_element_tree(fake_elem)
    assert 'not supported' in str(bad_by_exc.value)

    # Too many matches
    fake_elem.etree_locator = Locator(by=By.CSS_SELECTOR, value='p')
    fake_source_2 = f"<html><body><p>{fake_paragraph_txt}</p><p>unimportant</p></body></html>"
    mock_driver.page_source = fake_source_2
    with raises(SlimleafException) as too_many_results_exc:
        page.get_element_tree(fake_elem)
    assert 'Expected one' in str(too_many_results_exc.value)

    # No matches
    fake_elem.etree_locator = Locator(by=By.CSS_SELECTOR, value='a')
    with raises(SlimleafException) as no_results_exc:
        page.get_element_tree(fake_elem)
    assert 'No matching tree object' in str(no_results_exc.value)

    # Successful Tree generation
    mock_driver.page_source = fake_source_1  # Only one <p> tag
    fake_elem.etree_locator = Locator(by=By.CSS_SELECTOR, value='p')
    assert page.get_element_tree(fake_elem).text == fake_paragraph_txt
