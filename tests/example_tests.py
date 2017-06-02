from unittest import TestSuite, TestCase, TextTestRunner

from selenium import webdriver

from pages.xkcd.xkcd_pages import *


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
        xkcd_page = XKCDHome(self.driver)
        assert True  # An implicit assert is made behind the scenes to confirm we arrived safely

    def can_reach_store_using_link(self):
        xkcd_page = XKCDHome(self.driver)
        xkcd_page.store_link.click()
        xkcd_store = XKCDStore(self.driver, auto_get=False)  # The click already took us to the store, no get needed
        assert xkcd_store.footer_link.is_displayed()

    def can_pass_age_verification_on_register(self):
        """ User can continue with the registration process after choosing 'born before (date)'. """

        xkcd_registration = XKCDRegister(self.driver)
        xkcd_registration.valid_age_button.click()
        xkcd_terms = XKCDTermsAgreement(self.driver, auto_get=False)
        assert xkcd_terms.agree_to_terms_button.is_displayed()

    def forum_search_yields_expected_results(self):
        """ When searching the forums for posts, results are displayed. For accuracy this should be performed against a 
        non-production environment where tester has control of the data, e.g. posting against the forum and searching
        for that unique post. 
        """

        xkcd_forums = XKCDForum(self.driver)
        xkcd_forums.search_input.keyboard_input('Wszechczasów')  # This only works in a controlled test env
        xkcd_forums.search_submit_button.click()
        xkcd_search_results = XKCDSearchSingleResult(self.driver, auto_get=False)
        assert xkcd_search_results.selenium_search_results.is_displayed()


if __name__ == '__main__':
    testSet = TestSuite()
    testSet.addTests([TestSlimPOM('can_navigate_to_a_page_readably'), TestSlimPOM('can_reach_store_using_link'),
                      TestSlimPOM('can_pass_age_verification_on_register'),
                      TestSlimPOM('forum_search_yields_expected_results')])
    TextTestRunner().run(testSet)

