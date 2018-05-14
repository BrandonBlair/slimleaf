from unittest.mock import create_autospec

from pytest import fixture
from selenium import webdriver
from appium import webdriver as mobile_webdriver


@fixture(scope='session')
def mock_text():
    return 'test_text'


@fixture(scope='function')
def mock_driver():
    mocked_driver = create_autospec(webdriver.Chrome)
    return mocked_driver


@fixture(scope='function')
def mock_mobile_driver():
    mocked_mobile_driver = create_autospec(mobile_webdriver.Remote)
    return mocked_mobile_driver
