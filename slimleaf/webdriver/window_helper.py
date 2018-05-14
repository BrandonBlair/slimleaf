# Standard Imports
import logging

# Third Party Imports
from selenium.webdriver.support.wait import WebDriverWait

# Custom Imports

LOGGER = logging.getLogger(__name__)


class RegisteredWindowNameError(Exception):
    """ Error raised when using a common window name (like main) """
    pass


class WindowDoesNotExistError(Exception):
    """ Error raised when window does not exist """
    pass


class NoActiveWindowSessionException(Exception):
    """ Error raised when there are no active window sessions """
    pass


class IsPopupVisible(object):
    """ Expected Condition class for waiting until a popup is visible """

    def __init__(self, old_window):
        """
        :param string old_window: old_window lets us know where our main sess
                                  is located.
        """
        self.old_window = old_window

    def __call__(self, driver):
        """ Scan the number of windows and waits until there
        is more than one. """

        window_check = driver.window_handles
        return self.old_window != window_check[-1]


class WindowHelper(object):
    """ Window Helper helps manages active tabs

    Example of use:
        Clicking view payment link opens a link to a new tab/window.

        payment_link_css = "a.payment_link"
        window_helper = WindowHelper(driver)

        # Check the active session
        window_helper.active_session  # returns ('main', 'main_handle_hash')

        # Lets click the link now
        # Clicking the link would normally be
        # helper.find_click(driver, payment_link_css, elem_type=By.CSS_SELECTOR)
        # Use this method instead to store the window session
        window_helper.open_window(
            'payment_link_window',
            window_helper.find_click,
            driver,
            payment_link_css,
            elem_type=By.CSS_SELECTOR
        )

        # Check the active session
        window_helper.active_session
        # returns ('payment_link_window', 'payment_link_window_handle_hash')

        # If you want to run something on the main window before switching
        # back to the new tab, simply do
        window_helper.switch_to('main')
        window_helper.active_session  # returns ('main', 'main_handle_hash')
    """

    _MAIN_WINDOW_NAME = "main"

    def __init__(self, driver):
        self.driver = driver

        self._windows_in_session = dict()

        main_window_handle = self.driver.current_window_handle
        self._main_window = main_window_handle

        self._add_window(self._MAIN_WINDOW_NAME, main_window_handle)

    @property
    def active_session(self):
        """ Gets the active session from the private dictionary """
        for window_name, window_options in self._windows_in_session.items():
            if window_options['active']:
                return window_name, window_options['handle']
            else:
                continue  # pragma: no cover

        raise NoActiveWindowSessionException("There are no active windows")

    def _add_window(self, window_name, window_handle):
        """ Adds a new window to the sessions

        :param str window_name: What you want the session to be identified as
        :param str window_handle: The actual hash the driver uses to switch stuff

        example:
            window_hash = driver.window_handles[-1]
            window_name = 'new_window'

            window_helper._add_window(window_name, window_hash)
            window_name in window_helper._windows_in_session  # returns True
        """
        self._windows_in_session[window_name] = {
            "handle": window_handle,
            "active": True
        }

    def close_window(self, window_key):
        """ Attempts to close the window

        :param string window_key:

        example:
            window_helper.active_session  # returns ('settings_page', 'setting_hash')
            window_helper.close_window('settings_page')
            window_helper.active_session  # returns ('main', 'main_hash')
        """
        window_key = window_key.lower()

        if window_key == self._MAIN_WINDOW_NAME:
            raise AttributeError("Cannot close the main window")

        try:
            window_to_close = self._windows_in_session[window_key]['handle']
        except KeyError:
            err_msg = "Attempting to close a window that does not exist"
            raise WindowDoesNotExistError(err_msg)

        active_window_name, active_window_handle = self.active_session

        if active_window_handle == window_to_close:
            active_window_name = self._MAIN_WINDOW_NAME

        self.switch_to(window_key)

        # Closes tab/window
        self.driver.close()

        # Switches back to active and clears the key from windows dict
        self.switch_to(active_window_name)

        self._windows_in_session.pop(window_key, None)

    @property
    def current_sessions(self):
        """ Shows the current window names

        :rtype list:
        """
        return self._windows_in_session.keys()

    def _deactivate_all(self):
        """ Marks all the windows as unactive """

        for window_name in self._windows_in_session.keys():
            self._windows_in_session[window_name]['active'] = False

    def is_name_in_use(self, window_name):
        """ Checks if the name is in use or now

        :param str window_name: The name of the window you want to check
        """
        if window_name in self._windows_in_session:
            return True
        else:
            return False

    def open_window(self, window_name, func, *args, **kwargs):
        """ Opens the window and stores the session into our dictionary

        :param str window_name: what you want to name the session
        :param Function func: the function that will activate a click
        :param tuple *args: the func args
        :param dict **kwargs: the func kwargs

        example:
            helper.find_click will open a new window/tab when clicked

            window_helper.current_sessions  # returns ['main']
            window_helper.active_session   # returns ('main', 'main_hash')
            window_helper.open_window('page_1', helper.find_click, driver, 'link_xpath')
            window_helper.current_sessions  # returns ['main', 'page_1']
            window_helper.active_session   # returns ('page_1', 'page_1_hash')
        """

        window_name = window_name.lower()
        if window_name == self._MAIN_WINDOW_NAME:
            raise RegisteredWindowNameError("'main' window cannot be declared")
        elif self.is_name_in_use(window_name):
            msg = "'{0}' is already in use, use another or close the old one"
            raise RegisteredWindowNameError(msg.format(window_name))

        rval = func(*args, **kwargs)
        wait = WebDriverWait(self.driver, 30)
        wait.until(IsPopupVisible(self._main_window))

        window_handle = self.driver.window_handles[-1]
        self._deactivate_all()
        self._add_window(window_name, window_handle)

        return rval

    def switch_to(self, window_key):
        """ Switches to the given window

        :param str window_key:

        example:
            window_helper.current_sessions  # returns ['main', 'page_1', 'page_2']
            window_helper.active_session   # returns ('main', 'main_hash')
            window_helper.switch_to('page_2')
            window_helper.active_session   # returns ('page_2', 'page_2_hash')
        """
        try:
            # Getting the window handle and swapping to it
            window_key = window_key.lower()
            window_handle = self._windows_in_session[window_key]['handle']
            self.driver.switch_to_window(window_handle)

            # Deactiving all the windows
            self._deactivate_all()

            # Making the one swapped to active
            self._windows_in_session[window_key]['active'] = True
        except KeyError:
            err_msg = "Attempting to switch to window that does not exist"
            raise WindowDoesNotExistError(err_msg)
