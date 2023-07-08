import time
import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException

from .site_data.locators import BasePageLocators


class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)
        self.browser.maximize_window()

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, method, css_selector):
        try:
            self.browser.find_element(method, css_selector)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, method, css_selector, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).\
                until(EC.presence_of_element_located((method, css_selector)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, method, css_selector, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1). \
                until_not(EC.presence_of_element_located((method, css_selector)))
        except TimeoutException:
            return False
        return True
