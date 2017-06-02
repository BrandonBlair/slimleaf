from ..Page import Page
from selenium.webdriver.common.by import By


class XKCDHome(Page):

    url = 'https://www.xkcd.com'
    ready_element = {'by': By.CSS_SELECTOR, 'locator': "img[alt='xkcd.com logo']"}

    def __init__(self, driver):
        super().__init__(driver)  # Calls Page, which navigates to the URL we just set at the class level
        self.store_link = self.get_element(By.CSS_SELECTOR, "a[href='http://store.xkcd.com/']")


class XKCDStore(Page):

    url = 'https://store.xkcd.com/'
    ready_element = {'by': By.CSS_SELECTOR, 'locator': "img[alt='The xkcd store']"}

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.footer_link = self.get_element(By.XPATH, "//a[text()='The xkcd store']")


class XKCDForum(Page):

    url = 'http://forums.xkcd.com/'
    ready_element = {'by': By.CSS_SELECTOR, 'locator': 'a[title="Login"]'}

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.search_input = self.get_element(By.CSS_SELECTOR, '#keywords')
        self.search_submit_button = self.get_element(By.CSS_SELECTOR, 'button[title="Search"]')
        self.register_link = self.get_element(By.LINK_TEXT, 'Register')
        self.login_link = self.get_element(By.LINK_TEXT, 'Login')


class XKCDSearchSingleResult(Page):
    url = None  # Cannot arrive here directly without manually entering keyword to search against
    ready_element = {'by': By.CSS_SELECTOR, 'locator': 'h2[class="searchresults-title"]'}

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.selenium_search_results = self.get_element(By.XPATH, '//h2[text()="Search found 1 match: "]')


class XKCDRegister(Page):

    url = 'http://forums.xkcd.com/ucp.php?mode=register'
    ready_element = {'by': By.XPATH, 'locator': '//h2[text()="xkcd - Registration"]'}

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.valid_age_button = self.get_element(By.XPATH, '//a[contains(text(), "Before")]')


class XKCDTermsAgreement(Page):

    url = 'http://forums.xkcd.com/ucp.php?mode=register&coppa=0'  # This can be used to bypass age verification. Bug?
    ready_element = {'by': By.CSS_SELECTOR, 'locator': 'input[value="I agree to these terms"]'}

    def __init__(self, driver, **kwargs):
        super().__init__(driver, **kwargs)
        self.agree_to_terms_button = self.get_element(By.CSS_SELECTOR, 'input[value="I agree to these terms"]')
