from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable, presence_of_element_located)
from selenium.webdriver.support.select import Select

from appium.webdriver.common.touch_action import TouchAction

from slimleaf.webdriver.exceptions import (
    NotASelectElementException, NotAValidSelectOption, UnexpectedTagNameException,
    NoSuchElementException
)


class Element(object):
    """Base Element including useful functionality for manipulating elements

    Elements requiring additional/modified functionality should subclass this class. If a locator is
    static for a particular element, provide the _locator as a class attribute and the MobileElement
    can initialized without passing the locator argument.

    Args:
        driver (selenium.webdriver): Webdriver that will interface with the app
        locator (slimleaf.webdriver.locator.Locator): Locator used to find element
        web_element (selenium.webdriver.remote.webelement.WebElement): selenium web_element object
    """

    _locator = None

    def __init__(self, driver, locator=None, timeout=30, web_element=None, etree_locator=None):
        self.driver = driver
        self.locator = locator or self._locator
        self.timeout = timeout
        self.web_element = self.find()
        self.etree_locator = etree_locator

    def find(self):
        elem = WebDriverWait(self.driver, self.timeout).until(
            presence_of_element_located(self.locator)
        )
        return elem

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
        """Scrolls element into view (Web only)

        If an offset is desired, passing an integer (pixels) will scroll the Y axis accordingly.
        """

        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.web_element)
        if offset:
            self.driver.execute_script("window.scrollBy(0, {0});".format(offset))

    def click(self):
        elem = WebDriverWait(self.driver, self.timeout).until(
            element_to_be_clickable(self.locator)
        )
        elem.click()
        return None

    # Mobile actions
    def tap(self, x=5, y=5):
        touchable_elem = WebDriverWait(self.driver, self.timeout).until(
            element_to_be_clickable(self.locator)
        )
        touch_action = TouchAction(driver=self.driver)
        touch_action.tap(element=touchable_elem, x=x, y=y).perform()

    def swipe_left(self, x=5, y=5):
        self._swipe(-200, x, y)

    def swipe_right(self, x=5, y=5):
        self._swipe(200, x, y)

    def _swipe(self, pixels, x, y):
        elem = WebDriverWait(self.driver, self.timeout).until(
            element_to_be_clickable(self.locator)
        )
        touch_action = TouchAction(driver=self.driver)
        touch_action.press(elem, x, y).move_to(elem, x + pixels, y).release().perform()


class InputElement(Element):
    """Base Element for manipulating and validating input elements"""

    @property
    def text(self):
        """Text data from the input element, taken from the `value` attribute"""

        txt = self.web_element.get_attribute('value')
        return txt

    @text.setter
    def text(self, txt):
        """Sets the text for this input element as if a user had typed into it."""

        self.web_element.clear()
        self.web_element.send_keys(txt)
        return None


class CheckboxElement(InputElement):
    """Checkbox-style input element"""
    @property
    def is_checked(self):
        return self.web_element.get_attribute('checked') == 'checked'


class RadioField(object):
    """Radio fields consist of multiple input elements"""

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


class SelectElement(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.select_elem = Select(self.web_element)
        except UnexpectedTagNameException as e:
            raise NotASelectElementException from e

    @property
    def text(self):
        """Text value for first selected option in a dropdown (select) element"""

        selected_option = self.select_elem.first_selected_option
        return selected_option.text

    def choose(self, txt):
        try:
            self.select_elem.select_by_visible_text(txt)
        except NoSuchElementException as e:
            raise NotAValidSelectOption(
                f'Option {txt} is not present in existing options: {self.options}'
            ) from e

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


class AnchorElement(Element):
    """Represents an anchor element on a page"""

    pass
