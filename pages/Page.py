import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .WebElement import WebElement


class Page(object):
    """ The Page object enables readable, expressive manipulation of a selenium webdriver. While it appears to be a very
    thin wrapper over selenium functionality, it is highly customizable and newer testers can start writing tests
    quickly without ever touching the selenium API. Much of its power comes from the WebElement class. 
    """

    url = None
    ready_element = None

    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.driver.maximize_window()
        if kwargs.get('auto_get', True):
            self.get()  # Automatically navigate to this page's URL upon instantiation
        self.confirm_page_has_loaded()

    # Common browser functions
    def get(self):
        if self.get_current_url() == self.url:
            pass
        else:
            self.go_to(self.url)

    def confirm_page_has_loaded(self):
        ready_element = self.get_element(self.ready_element['by'], self.ready_element['locator'])
        assert ready_element.is_displayed()

    def go_to(self, url):
        print(f"Navigating to URL: {url}")  # Can make test runs more expressive. Implement logger for customized output
        self.driver.get(url)

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()

    def close(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def text_exists(self, expected_text):
        return expected_text in self.driver.page_source

    def get_element(self, by, val, **kwargs):
        return WebElement(self.driver, by, val, **kwargs)

    def wait_for_element(self, by, locator, *, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))

    def element_is_displayed(self, element):
        self.wait_for_element(element.by, element.locator)
        return self.driver.find_element(element.by, element.locator).is_displayed()
