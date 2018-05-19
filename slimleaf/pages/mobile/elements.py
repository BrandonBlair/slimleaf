
from slimleaf.pages.element import Element
from slimleaf.webdriver.exceptions import AttributeNotFoundException


class SwitchElement(Element):
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
