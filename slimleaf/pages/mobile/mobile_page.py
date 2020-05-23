from appium.common.exceptions import NoSuchContextException

from selenium.common.exceptions import WebDriverException

from slimleaf.exceptions import SlimleafException
from slimleaf.pages.page import Page

WEBVIEW_CONTEXT = 'WEBVIEW'
NATIVE_CONTEXT = 'NATIVE_APP'


class PageMismatchException(SlimleafException):
    pass


class MobilePage(Page):
    """Base Page containing useful functionality for describing a particular mobile screen.

    Page Objects should be subclassed from BasePage, with customized methods extending or overriding
    the existing ones.

    Attributes:
        context (str): NATIVE, WEBVIEW, etc. Allows hybrid app support
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context != self.required_context:
            self.switch_to_required_context()

        if not self.is_current_page:
            raise PageMismatchException(f"{self.unique_locator} not found")

    @property
    def required_context(self):
        """In hybrid apps, some pages use the NATIVE_APP context, and some use the WEBVIEW context.

        If a particular context is required for the current page, overriding this allows context
        switching to occur in the background with no user intervention. This is a property because
        in the case of WEBVIEW contexts, extra logic is necessary to retrieve the ID, requiring that
        the object be initialized already.
        """

        return NATIVE_CONTEXT

    @property
    def contexts(self):
        contxts = wait_through_exception_then_return(
            exc=WebDriverException, func=self.driver.contexts
        )
        return contxts

    @property
    def context(self):
        return self.driver.current_context

    @property
    def webview_id(self):
        for con in self.contexts:
            if WEBVIEW_CONTEXT in con:
                return con
        raise SlimleafException(
            f'No webview for this page. Available contexts: {self.contexts}'
        )

    def switch_to_required_context(self):
        try:
            self.driver.switch_to.context(self.required_context)
        except NoSuchContextException:
            available_contexts = self.driver.contexts
            raise SlimleafException(
                f'Context {self.context} does not match available contexts {available_contexts}'
            )
        return None

    def scroll_down(self):
        self._scroll("down")

    def scroll_up(self):
        self._scroll("up")

    def _scroll(self, direction):
        """Scroll screen in a direction

        Args:
            direction (str): e.g. "down"
        """

        if direction not in ['up', 'down']:
            raise SlimleafException("Supported scroll directions are 'up' and 'down'")

        self.driver.execute_script("mobile: scroll", {"direction": direction})
