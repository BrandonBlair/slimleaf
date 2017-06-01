from unittest import TestSuite, TestCase, TextTestRunner

from selenium import webdriver

from pages.xkcd.xkcd_pages import XKCDHome, XKCDStore


class TestSlimPOM(TestCase):
    """ Requires a Firefox webdriver be installed and included in your path per Selenium 3 docs. """

    def setUp(self):
        """ The shared driver is only used for convenience here - sharing class attributes across an entire test run
        isn't recommended as it makes test isolation impossible. 
        """

        self.driver = webdriver.Firefox()
        #self.driver = webdriver.PhantomJS()

    def tearDown(self):
        self.driver.quit()  # driver.close() doesn't work reliably on some browsers (looking at you, Firefox)

    def can_navigate_to_a_page_readably(self):
        xkcd_page = XKCDHome(self.driver)  # An implicit assert is made behind the scenes to confirm we arrived safely
        assert xkcd_page.get_title().startswith('xkcd')

    def can_reach_store_using_link(self):
        xkcd_page = XKCDHome(self.driver)
        xkcd_page.store_link.click()
        xkcd_store = XKCDStore(self.driver, auto_get=False)  # The click already took us to the store, no get needed
        assert xkcd_store.footer_link.is_displayed()


if __name__ == '__main__':
    testSet = TestSuite()
    testSet.addTests([TestSlimPOM('can_navigate_to_a_page_readably'), TestSlimPOM('can_reach_store_using_link')])
    TextTestRunner().run(testSet)

