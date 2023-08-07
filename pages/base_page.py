from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, env='', url='', timeout=10):
        self.env = env
        self.browser = browser
        self.url = url
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

    def is_clickable(self, method, css_selector, element_for_format='', timeout=4):
        try:
            WebDriverWait(self.browser, timeout). \
                until(EC.element_to_be_clickable((method, css_selector.format(element_for_format))))
        except TimeoutException:
            error_text = f'Element is not clickable: "{css_selector.format(element_for_format)}"'
            print(error_text, end=' ')
            raise TimeoutException(error_text)
        return self.find_elem(method, css_selector, element_for_format=element_for_format)

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

    def is_disappeared(self, method, css_selector, element_for_format='', error_text='', timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1). \
                until_not(EC.presence_of_element_located((method, css_selector.format(element_for_format))))
        except TimeoutException:
            return False
        return True
