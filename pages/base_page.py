from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .site_data.locators import BasePageLocators as BPLocator


class BasePage:
    def __init__(self, browser, env='', url='', timeout=10):
        self.env = env
        self.browser = browser
        self.url = url
        self.implicitly_wait_timeout = timeout
        self.browser.implicitly_wait(timeout)
        self.browser.maximize_window()

    def open(self):
        self.browser.get(self.url)

    def find_elem(self, method, css_selector, element_for_format=(), error_text=''):
        found_elem = self.browser.find_elements(method, css_selector.format(*element_for_format))
        if len(found_elem) == 0:
            if error_text:
                print_text = error_text
            else:
                print_text = f'[No Such Element by {method}: "{css_selector.format(*element_for_format)}"]'
            print(print_text, end=' ')
            assert False, print_text
        else:
            return found_elem[0]

    def is_clickable(self, method, css_selector, element_for_format=(), timeout=4):
        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout). \
                until(EC.element_to_be_clickable((method, css_selector.format(*element_for_format))))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            error_text = f'Element is not clickable: "{css_selector.format(*element_for_format)}"'
            print(error_text, end=' ')
            raise TimeoutException(error_text)
        return self.find_elem(method, css_selector, element_for_format=element_for_format)

    def is_element_present(self, method, css_selector, element_for_format=()):
        try:
            self.browser.find_element(method, css_selector.format(*element_for_format))
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, method, css_selector, element_for_format=(), error_text='', timeout=4):
        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout).\
                until(EC.presence_of_element_located((method, css_selector.format(*element_for_format))))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, method, css_selector, element_for_format=(), error_text='', timeout=4):
        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout=timeout). \
                until_not(EC.visibility_of_element_located((method, css_selector.format(*element_for_format))))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            return False
        return True

    def is_url_contains(self, url, timeout=4):
        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout).\
                until(EC.url_contains(url))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            return False
        return True

    def should_be_sidebar(self):
        self.find_elem(*BPLocator.SIDEBAR)
        self.find_elem(*BPLocator.PROJECT_SELECTOR)
        self.find_elem(*BPLocator.ALL_SCENARIOS_BUTTON)
        self.find_elem(*BPLocator.OPEN_MENU_BUTTON)

    def choose_project(self, project_name):
        self.find_elem(*BPLocator.PROJECT_SELECTOR).click()
        self.is_clickable(*BPLocator.ITEM_IN_SELECTOR, element_for_format=(project_name,)).click()

        project_selector_text = self.find_elem(*BPLocator.PROJECT_SELECTOR).text
        assert project_name == project_selector_text, \
            f'Project name: "{project_name}" not in project selector, project selector have: "{project_selector_text}"'


