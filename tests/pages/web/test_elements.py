from unittest.mock import patch, MagicMock

from selenium.webdriver.common.by import By
from pytest import raises

from slimleaf.pages.web import elements
from slimleaf.webdriver.locator import Locator


TEST_LOCTR = Locator(by=By.CSS_SELECTOR, value="unimportant")


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_elements(_mock_wait, mock_driver):
    base_element = elements.BaseElement(driver=mock_driver, locator=TEST_LOCTR, timeout=5)

    _mock_wait.assert_called_once()

    base_element.click()
    base_element.text
    base_element.is_displayed
    base_element.scroll_into_view(offset=200)


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_input_element(_mock_wait, mock_text, mock_driver):
    mock_elem = MagicMock()
    mock_elem.get_attribute.return_value = mock_text
    _mock_wait.return_value.until.return_value = mock_elem

    input_element = elements.InputElement(mock_driver, TEST_LOCTR)
    assert input_element.text == mock_text  # Validate property is used

    input_element.text = 'unimportant'
    input_element.web_element.clear.assert_called_once()


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_checkbox_element(_mock_wait, mock_driver):
    mock_elem = MagicMock()
    _mock_wait.return_value = mock_elem

    checkbox_element = elements.CheckboxElement(mock_driver, TEST_LOCTR)
    checkbox_element.is_checked
    checkbox_element.web_element.get_attribute.assert_called_once()


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_radio_input_element(_mock_wait, mock_driver):
    mock_elem = MagicMock()
    _mock_wait.return_value = mock_elem

    radio_element = elements.RadioInputElement(mock_driver, TEST_LOCTR)
    radio_element.selected
    radio_element.web_element.is_selected.assert_called_once()


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_radio_field_element(_mock_wait, mock_driver):
    mock_elem = MagicMock()
    mock_elem.selected = True
    _mock_wait.return_value = mock_elem

    radio_field_elem = elements.RadioField()
    radio_field_elem.add_input(mock_elem)
    assert radio_field_elem.selected == mock_elem


@patch('slimleaf.pages.web.elements.Select')
@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_select_element(_mock_wait, _mock_select, mock_text, mock_driver):
    mock_elem = MagicMock()
    _mock_wait.return_value = mock_elem

    # Create mock Select which will be an attribute of the SelectElement class
    mock_select_elem = MagicMock()
    option_elem = MagicMock()
    option_elem.text = mock_text
    mock_select_elem.first_selected_option = option_elem
    mock_select_elem.options = [option_elem]
    _mock_select.return_value = mock_select_elem

    select_element = elements.SelectElement(mock_driver, TEST_LOCTR)
    assert select_element.text == mock_text

    select_element.choose('unimportant')
    select_element.select_elem.select_by_visible_text.assert_called_once()
    assert select_element.options == [mock_text]


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_unchanged_element_classes(_mock_wait, mock_driver):
    mock_elem = MagicMock()
    _mock_wait.return_value = mock_elem

    # If these instantiate without exceptions, consider them validated. Currently only pass-throughs
    try:
        elements.LabelElement(mock_driver, TEST_LOCTR)
        elements.ButtonElement(mock_driver, TEST_LOCTR)
        elements.LinkElement(mock_driver, TEST_LOCTR)
        assert True
    except Exception:
        assert False


@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_modal_element(_mock_wait, mock_driver):

    mock_elem = MagicMock()
    _mock_wait.return_value = mock_elem
    modal_elem = elements.ModalElement(mock_driver, TEST_LOCTR)
    with raises(NotImplementedError):
        modal_elem.is_displayed()
    with raises(NotImplementedError):
        modal_elem.close_button()


@patch('slimleaf.pages.web.elements.ActionChains')
@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_menu_element(_mock_wait, _mock_action, mock_text, mock_driver):
    class MockMenuElement(elements.MenuElement):
        @property
        def options(self):
            return [mock_text]

    mock_elem = MagicMock()
    _mock_wait.return_value = mock_elem
    menu_elem = MockMenuElement(mock_driver, TEST_LOCTR)
    options = menu_elem.hover(return_options=True)
    _mock_action.assert_called_once()
    assert options == [mock_text]


@patch('slimleaf.pages.web.elements.re')
@patch('slimleaf.pages.web.elements.WebDriverWait')
def test_header_element(_mock_wait, _mock_re, mock_text, mock_driver):
    mock_elem = MagicMock()
    mock_elem.value_of_css_property.return_value = mock_text
    _mock_wait.return_value.until.return_value = mock_elem

    header_elem = elements.HeaderElement(mock_driver, TEST_LOCTR)

    # Validate color logic
    assert header_elem.color == mock_text
    mock_elem.value_of_css_property.assert_called_once()

    # Validate transparency logic
    mock_elem.reset_mock()
    header_elem.transparency
    mock_elem.value_of_css_property.assert_called_once()
