import re
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import UnexpectedTagNameException, NoSuchElementException
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable, presence_of_element_located)
from selenium.webdriver.support.wait import WebDriverWait

from slimleaf.exceptions import SlimleafException


class Element(object):
    """Base Element including useful functionality for manipulating web elements

    Elements requiring additional/modified functionality should subclass this class. If a locator is
    static for a particular element, provide the locator as a class attribute and the Element
    can initialized without passing the locator argument.

    Args:
        driver (selenium.webdriver): Webdriver that will interface with the web
        locator (slimleaf.webdriver.locator.Locator): Locator used to find element
        etree_locator (slimleaf.webdriver.locator.Locator); Locator used to find lxml element trees
        timeout (int): Duration (seconds) to wait for an element before a TimeoutException is raised
        web_element (selenium.webdriver.remote.webelement.WebElement): selenium-level web_element
    """

    _locator = None
    _etree_locator = None

    def __init__(self, driver, locator=None, etree_locator=None, timeout=30, web_element=None):
        self.driver = driver
        self.locator = locator or self._locator
        self.timeout = timeout
        self.web_element = self.find()
        self.etree_locator = etree_locator or self._etree_locator

    def find(self):
        elem = WebDriverWait(self.driver, self.timeout).until(
            presence_of_element_located(self.locator)
        )
        return elem

    def click(self):
        elem = WebDriverWait(self.driver, self.timeout).until(
            element_to_be_clickable(self.locator)
        )
        elem.click()
        return None

    @property
    def text(self):
        """Represents the text data of an element.

        If additional steps are required to retrieve the desired text - e.g. the value attribute of
        an element - this method should be subclassed.
        """
        txt = self.web_element.text
        return txt

    @property
    def is_displayed(self):
        return self.web_element.is_displayed()

    def scroll_into_view(self, offset=None):
        """Scrolls element into view.

        If an offset is desired, passing an integer (pixels) will scroll the Y axis accordingly.
        """

        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.web_element)
        if offset:
            self.driver.execute_script("window.scrollBy(0, {0});".format(offset))


class InputElement(Element):
    """Base Element for manipulating and validating input elements"""

    @property
    def text(self):
        """Text data from the input element, taken from the `value` attribute"""

        txt = self.web_element.get_attribute('value')
        return txt


    def clear(self):
        """Clears the content of currently active input field"""

        self.web_element.clear()
        return None


    @text.setter
    def text(self, txt):
        """Sets the text for this input element as if a user had typed into it."""

        self.clear()
        self.web_element.send_keys(txt)
        return None


class CheckboxElement(InputElement):
    """Checkbox-style input element"""
    @property
    def is_checked(self):
        return self.web_element.get_attribute('checked') == 'checked'


class RadioField(object):
    """Radio field for webpages"""

    def __init__(self):
        self.inputs = []

    def add_input(self, input_element):
        self.inputs.append(input_element)

    @property
    def selected(self, multi=False):
        """Returns all selected inputs. If multi is set to False, only the first is returned."""
        selected_inputs = [input_elem for input_elem in self.inputs if input_elem.selected]
        selected_input = selected_inputs if multi else selected_inputs[0]
        return selected_input


class RadioInputElement(InputElement):
    """Base element for manipulating and validating radio-style input elements"""

    @property
    def selected(self):
        return self.web_element.is_selected()


class NotAValidSelectOption(SlimleafException):
    pass


class NoSuchElementException(SlimleafException):
    pass


class NotASelectElementException(SlimleafException):
    pass


class SelectElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.select_elem = Select(self.web_element)
        except UnexpectedTagNameException as e:
            raise NotASelectElementException(self.web_element.tag_name) from e

    @property
    def text(self):
        """Text value for first selected option in a dropdown (select) element"""

        selected_option = self.select_elem.first_selected_option
        return selected_option.text

    def choose(self, txt):
        try:
            self.select_elem.select_by_visible_text(txt)
        except NoSuchElementException as e:
            raise NotAValidSelectOption(txt) from e

    @property
    def options(self):
        option_txt = [elem.text for elem in self.select_elem.options]
        return option_txt


class LabelElement(Element):
    """Currently no extended functionality beyond Element."""
    pass


class ButtonElement(Element):
    """Currently no extended functionality beyond Element."""

    pass


class LinkElement(Element):
    """Currently no extended functionality beyond Element."""

    pass


class ModalElement(Element):
    """Element representing a modal on the page.

    The following methods must be overridden:
        - is_displayed
        - close_button
    """

    def is_displayed(self):
        raise NotImplementedError()

    def close_button(self):
        raise NotImplementedError()


class MenuElement(Element):
    """ Class that lets the user manipulate a dropdown menu"""

    @property
    def options(self):
        pass  # pragma: no cover

    def hover(self, return_options=True):
        """Moves to element to activate the dropdown and can return dropdown options"""
        actions = ActionChains(self.driver)
        actions.move_to_element(self.web_element)
        actions.click(self.web_element)
        actions.perform()

        if return_options:
            return self.options


class AnchorElement(Element):
    """Represents an anchor element on a page"""

    pass
