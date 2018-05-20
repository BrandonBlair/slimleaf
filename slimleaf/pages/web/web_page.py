from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located, staleness_of)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from slimleaf.webdriver.exceptions import PageMismatchException
from slimleaf.pages.page import Page


class WebPage(Page):
    """Base Page containing useful functionality for describing a Web Page

    Page Objects should be subclassed from BasePage, with customized methods extending or overriding
    the existing ones.

    Attributes:
        path (str): url path (not including domain) used to locate this particular page
        title (str): Title of a page
        url (str): Absolute url comprised of scheme, domains, and path to resource
    """

    path = ''

    def __init__(self, base_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    @property
    def url(self):
        """The absolute URL of the page

        Because the same page can have different URLs between environments, and even at different
        stages of access, building the URL at run-time is much safer than assuming it never changes.
        """

        absolute_url = f"{self.base_url}{self.path}"
        return absolute_url

    # Browser interactions
    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        """The current URL as reported by Selenium WebDriver"""

        return self.driver.current_url

    def go(self):
        """Navigate to this page using a webdriver

        In cases where this page is only reached via navigating from another page, and cannot
        be reached via typing a URL into the web, this should not be used.
        """

        self.driver.get(self.url)
        if not self.is_current_page:
            raise PageMismatchException(
                "Expected to arrive at {expected} but arrived at {actual} instead.".format(
                    expected=self.url,
                    actual=self.driver.current_url
                )
            )
        return self  # Allows chaining, e.g. `page = BasePage(driver).go()`

    def back(self):
        """Equivalent of clicking Back on a browser UI"""

        self.driver.back()
        return None

    def forward(self):
        """Equivalent of clicking Forward on a browser UI"""

        self.driver.forward()
        return None

    def refresh(self, timeout=30):
        """Refreshes the current page in the browser

        Waiting for the html element to go stale ensures the refresh is complete and avoids
        proceeding too early.
        """

        locator = (By.CSS_SELECTOR, 'html')
        html_elem = WebDriverWait(self.driver, timeout).until(presence_of_element_located(locator))
        self.driver.refresh()

        # Wait until previous element has gone stale
        WebDriverWait(self.driver, timeout).until(staleness_of(html_elem))
        return None

    def close(self):
        """Closes the current window handle"""

        self.driver.close()
        return None

    # Scrolling
    def scroll_to_bottom(self):
        """Scroll to the bottom of the window"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return None

    def scroll_to_center(self):
        """Scroll to the center of the window"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        return None

    def scroll_to_top(self):
        """Scroll to the top of the window"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        return None

    # Window/Tab handling
    @property
    def open_windows(self):
        open_handles = self.driver.window_handles
        return list(open_handles)

    def switch_to_newest_window(self):
        newest_window = self.driver.window_handles[-1]
        self.switch_to_window(newest_window)
        return None

    def switch_to_oldest_window(self):
        oldest_window = self.driver.window_handles[0]
        self.switch_to_window(oldest_window)
        return None

    def switch_to_window(self, handle):
        self.driver.switch_to.window(handle)
        return None
