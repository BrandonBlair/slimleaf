from lxml import etree

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from slimleaf.exceptions import SlimleafException


class Page(object):
    """Page object allowing simple, expressive interactions with a web page or mobile screen.

    All domain-specific page classes should inherite from Page.

    Attributes:
        unique_locator (slimleaf.webdriver.locator.Locator): locator for an element unique to
            this page, which will be used to identify whether or not page is currently displayed.
        driver (selenium.webdriver): Webdriver that will interface with the web
        is_current_page (bool): If the page herein described is currently displayed in the web
        html_tree (lxml.etree.ElementBase): lxml tree for rapid and efficient parsing of complex
        element trees

    Args:
        driver
    """

    def __init__(self, driver):
        self.driver = driver

    @property
    def unique_locator(self):
        """Locator describing an element that is unique to the current page (screen). Checking
        if this element is displayed is more reliable than checking against url, title, etc.
        """

        pass  # pragma no cover

    @property
    def is_current_page(self):
        """Describe whether this page is currently displayed in the webdriver instance.

        Since URLS are often hidden by endpoint paths and page titles are not guaranteed to be
        unique, these are unsuitable for validation. The most reliable method is to identify an
        element that is...
            1. unique to the page
            2. unlikely to change
        ...and try to locate it.
        """

        try:
            WebDriverWait(self.driver, 30).until(
                presence_of_element_located(self.unique_locator)
            )
            return True
        except TimeoutException:
            return False

    @property
    def html_tree(self):
        """Retrieve page source as lxml tree for fast, efficient data retrieval

        Returns:
            tree (lxml.etree.Element): lxml tree object for hierarchical data retrieval
        """

        parser = etree.HTMLParser(encoding='utf-8')
        xml = self.driver.page_source.encode('utf-8')
        tree = etree.fromstring(xml, parser=parser)
        return tree

    def get_element_tree(self, element):
        """Retrieve an lxml tree object for a specific element

        Args:
            element (slimleaf.pages.element.Element): Element from which tree is built

        Returns:
            tree (lxml.etree.Element) lxml tree with a root matching that of the element
        """

        SUPPORTED_BYS = [By.CSS_SELECTOR, By.XPATH]

        trees = None
        if not hasattr(element, 'etree_locator'):
            raise SlimleafException(f'Element {element} does not have an etree locator')

        elif element.etree_locator.by not in SUPPORTED_BYS:
            raise SlimleafException(
                f"Element's etree locator {element.etree_locator.by} not supported. Supported by's "
                f"are {SUPPORTED_BYS}"
            )

        else:
            loctr = element.etree_locator
            if loctr.by == By.CSS_SELECTOR:
                trees = self.html_tree.cssselect(loctr.value)
            elif loctr.by == By.XPATH:
                trees = self.html_tree.xpath(loctr.value)

        if not trees:
            raise SlimleafException(
                f'No matching tree object found for element {element} using locator '
                f'{element.etree_locator}.'
            )

        elif len(trees) != 1:
            raise SlimleafException(
                f'Expected one matching element tree, found {len(trees)}: {trees}'
            )

        else:
            return trees[0]
