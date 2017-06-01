from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


class WebElement(object):
    """ The WebElement is a small but powerful (and highly extensible) wrapper around selenium's Element. It addresses 
    common causes of brittle and/or inconsistent tests, and exposes clear, readable, intuitive functions to users. It
    is also an expression of how you want automated browser tests to be written, as good practices can be made simpler
    and bad practices more difficult (via omission).
    """

    def __init__(self, driver, by, val, **kwargs):
        self.timeout = kwargs.get('timeout') or 30
        self.driver = driver
        self.by = by
        self.locator = val

        # Explicit waits on each element can make tests less brittle when elements are slow to load.
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((self.by, self.locator)))

        # To handle more complex tests, implement finding multiple elements per locator.
        self.selenium_element = self.driver.find_element(by, val)

    def click(self, **kwargs):
        """ Clicking is a great example of the necessity of wrapping selenium driver functionality in custom functions.
        Relying on selenium's default click functionality causes brittle tests in the case of elements that are slow to
        load, browsers that misbehave when clicking the exact center (0, 0) of a button, etc. Implementing some basic
        logic can minimize misleading failures arising from test execution (not helpful) as opposed to failures that
        arise from the system under test (very helpful).
        """

        timeout = kwargs.get('timeout') or 10  # Build in some leeway to avoid brittle tests
        offset = kwargs.get('offset')

        # Waiting for each element to become clickable decreases brittleness of tests.
        clickable_element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((self.by, self.locator)))

        # Some elements have issues clicking in middle, offset solves this
        if offset:
            ActionChains(self.driver).move_to_element_with_offset(clickable_element, 0, offset).click().perform()
        else:
            clickable_element.click()

    def keyboard_input(self, txt, *, clear_first=False):
        """ When sending keys to a specific element we sometimes care about typing into an empty field, and sometimes
         do not. Passing clear_first=True will attempt to clear the field first. 
         """

        if clear_first:
            self.selenium_element.clear()
        self.selenium_element.send_keys(txt)

    def get_text(self):
        return self.selenium_element.text

    def get_attribute(self, attr_name):
        """ While wrapping get_attribute without adding logic seems frivolous, ideally I do not want testers having to
        dig into the selenium API unless absolutely necessary. Wrapping this helps readability at the test case level.
        """

        return self.selenium_element.get_attribute(attr_name)

    def select_dropdown_option(self, value, *, select_by):
        """ Selects a particular element inside a dropdown, either by text, index, or value. """

        if select_by not in ['text', 'index', 'value']:
            raise ValueError('Must select by either text, index, or value to interact with dropdown elements')

        dropdown = Select(self.selenium_element)
        if select_by == 'text':
            dropdown.select_by_visible_text(value)
        elif select_by == 'index':
            dropdown.select_by_index(value)
        elif select_by == 'value':
            dropdown.select_by_value(value)

    def is_displayed(self):
        return self.selenium_element.is_displayed()

    def get_dropdown_options(self):
        return [option.text for option in self.selenium_element.find_elements_by_tag_name("option")]