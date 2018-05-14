from unittest.mock import MagicMock, patch

from slimleaf.pages.mobile.elements import BaseElement, InputElement, ButtonElement
from slimleaf.webdriver.locator import Locator
from appium.webdriver.common.mobileby import MobileBy


@patch('slimleaf.pages.mobile.elements.WebDriverWait')
@patch('slimleaf.pages.mobile.elements.TouchAction')
def test_base_element(_mock_touch_action, _mock_wait, mock_text, mock_driver):
    mock_elem = MagicMock()
    mock_elem.text = mock_text
    _mock_wait.return_value.until.return_value = mock_elem
    elem_loctr = Locator(MobileBy.IOS_PREDICATE, 'type == XCUIElementTypeStaticText')

    text_elem = BaseElement(driver=mock_driver, locator=elem_loctr)
    text_elem.is_displayed()

    assert text_elem.text == mock_text
    text_elem.is_displayed.assert_called_once()


@patch('slimleaf.pages.mobile.elements.WebDriverWait')
@patch('slimleaf.pages.mobile.elements.TouchAction')
def test_input_element(_mock_touch_action, _mock_wait, mock_text, mock_driver):
    mock_elem = MagicMock()
    mock_elem.get_attribute.return_value = mock_text
    _mock_wait.return_value.until.return_value = mock_elem
    input_loctr = Locator(MobileBy.IOS_PREDICATE, 'type == XCUIElementTypeTextField')

    input_elem = InputElement(driver=mock_driver, locator=input_loctr, timeout=2)
    input_elem.tap(x=5, y=5)
    _mock_touch_action.assert_called_once()
    assert input_elem.text == mock_text

    input_elem.text = mock_text  # Calls setter
    input_elem.clear()

    assert issubclass(ButtonElement, BaseElement)
