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



