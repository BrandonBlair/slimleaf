from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable, presence_of_element_located)
from selenium.webdriver.support.wait import WebDriverWait

from slimleaf.webdriver.exceptions import AttributeNotFoundException


class BaseElement(object):
    """Base Element including useful functionality for manipulating mobile elements

    Elements requiring additional/modified functionality should subclass this class. If a locator is
    static for a particular element, provide the locator as a class attribute and the BaseElement
    can initialized without passing the locator argument.

    Args:
        driver (selenium.webdriver): Webdriver that will interface with the app
        locator (slimleaf.webdriver.locator.Locator): Locator used to find element
        web_element (selenium.webdriver.remote.webelement.WebElement): selenium-level web_element
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


class InputElement(BaseElement):
    """Base Element for manipulating and validating input elements"""

    def __init__(self, *args, default_text='', **kwargs):
        self.default_text = default_text
        super().__init__(*args, **kwargs)

    @property
    def text(self):
        """Text data from the input element, taken from the `value` attribute"""

        txt = self.web_element.get_attribute('value')
        return txt

    @text.setter
    def text(self, txt):
        """Sets the text for this input element as if a user had typed into it."""

        self.web_element.send_keys(txt)
        return None

    def clear(self):
        """Clears text from an input field"""

        self.web_element.clear()
        return None


class SwitchElement(BaseElement):
    """Base Element for manipulating and validating input elements"""

    @property
    def on(self):
        """Is the switch set to the `on` position? Derived from value attribute."""
        val = self.web_element.get_attribute('value')
        if val is None:
            raise AttributeNotFoundException(
                f"Element with locator {self.locator} has no value attribute"
            )
        else:
            return int(val) == 1


class ButtonElement(BaseElement):
    pass
