import inspect

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.site_data.locators import BasePageLocators as BPLocator

from custom_moduls import custom_expected_conditions as CEC
from custom_moduls.console_design.colors import ConsoleColors as CCol
from custom_moduls.console_design.link_to_modules import print_link_to_modules as print_link


def assert_error(error_text, method=None, css_selector=''):

    f_back = inspect.currentframe().f_back.f_back
    link = print_link(file=f_back.f_code.co_filename, line=f_back.f_lineno)
    code_obj_name = f_back.f_code.co_name
    print_text_error = f'\r{link}[{CCol.txt_blu(code_obj_name)}] '

    if error_text:
        print_text_error += error_text
    else:
        print_text_error += (f'No Such Element by {CCol.txt_yel(method)}: '
                             f'"{CCol.txt_vio(css_selector)}"')
    assert False, print_text_error


class BasePage:
    def __init__(self, browser, env='', url='', timeout=10, language='en'):
        self.env = env
        self.browser = browser
        self.url = url
        self.language = language
        self.implicitly_wait_timeout = timeout
        self.browser.implicitly_wait(timeout)
        self.browser.maximize_window()

    def open(self):
        self.browser.get(self.url)

    def find_elem(self, method, css_selector, element_for_format=(), error_text='', elem_id=0, timeout=None):

        css_selector = css_selector.format(*element_for_format)

        if timeout is not None:
            self.browser.implicitly_wait(timeout)
        found_elements = self.browser.find_elements(method, css_selector)
        self.browser.implicitly_wait(self.implicitly_wait_timeout)

        if len(found_elements) == 0:
            assert_error(error_text, method=method, css_selector=css_selector)

        return found_elements[elem_id]

    def scroll_to_element(self, method, css_selector, element_for_format=(), error_text='', elem_id=0, timeout=None):

        css_selector = css_selector.format(*element_for_format)

        if timeout is not None:
            self.browser.implicitly_wait(timeout)
        found_elements = self.browser.find_elements(method, css_selector)
        self.browser.implicitly_wait(self.implicitly_wait_timeout)

        if len(found_elements) == 0:
            assert_error(error_text, method=method, css_selector=css_selector)

        self.browser.execute_script("arguments[0].scrollIntoView();", found_elements[elem_id])
        return found_elements[elem_id]

    def scroll_in_element(self, method, css_selector, element_for_format=(),
                          error_text='', elem_id=0, direction='DOWN', timeout=None):

        css_selector = css_selector.format(*element_for_format)

        if timeout is not None:
            self.browser.implicitly_wait(timeout)
        found_elements = self.browser.find_elements(method, css_selector)
        self.browser.implicitly_wait(self.implicitly_wait_timeout)

        if len(found_elements) == 0:
            assert_error(error_text, method=method, css_selector=css_selector)
        elif direction == 'DOWN':
            self.browser.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);",
                                        found_elements[elem_id])
        elif direction == 'UP':
            self.browser.execute_script("arguments[0].scroll(0, arguments[0].scrollIntoView());",
                                        found_elements[elem_id])
        else:
            assert_error(error_text=f'Wrong direction for scrolling in element: "{CCol.txt_vio(css_selector)}"')

        return found_elements[elem_id]

    def is_clickable(self, method, css_selector, element_for_format=(), timeout=4, return_bool=False):
        # def click(elem):
        #     elem.click()

        css_selector = css_selector.format(*element_for_format)

        try:
            self.browser.implicitly_wait(0)
            element = WebDriverWait(self.browser, timeout=timeout). \
                until(EC.element_to_be_clickable((method, css_selector)))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
            # click(element)
            return element
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=f'Element is not clickable: "{CCol.txt_vio(css_selector)}"')
            else:
                return False

    def is_element_scroll_height(self, method, css_selector, expected_scroll_height,
                                 element_for_format=(), error_text='', timeout=4):

        css_selector = css_selector.format(*element_for_format)

        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout=timeout). \
                until(CEC.element_has_scroll_size(css_selector, expected_scroll_height))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            if error_text == '':
                error_text = (f'Scroll height by element: "{CCol.txt_vio(css_selector)}" '
                              f'lower then expected scroll height: "{CCol.txt_vio(expected_scroll_height)}"')
            assert_error(error_text=error_text)
        return True

    def is_not_element_present(self, method, css_selector, element_for_format=(),
                               error_text='', timeout=4, return_bool=False):

        css_selector = css_selector.format(*element_for_format)

        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout=timeout). \
                until(EC.presence_of_element_located((method, css_selector)))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            return True
        if not return_bool:
            assert_error(error_text=error_text)
        else:
            return False

    def is_element_contains_text(self, method, css_selector, element_for_format=(),
                                 error_text='', timeout=4, return_bool=False,  text=''):

        css_selector = css_selector.format(*element_for_format)

        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout=timeout). \
                until_not(EC.text_to_be_present_in_element((method, css_selector), text))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=error_text)
            else:
                return False
        return True

    def is_disappeared(self, method, css_selector, element_for_format=(), error_text='', timeout=4, return_bool=False):

        css_selector = css_selector.format(*element_for_format)

        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout=timeout). \
                until_not(EC.visibility_of_element_located((method, css_selector)))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=error_text)
            else:
                return False
        return True

    def is_url_contains(self, text_from_url, error_text='', timeout=4, return_bool=False):
        try:
            self.browser.implicitly_wait(0)
            WebDriverWait(self.browser, timeout=timeout). \
                until(EC.url_contains(text_from_url))
            self.browser.implicitly_wait(self.implicitly_wait_timeout)
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=error_text)
            else:
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
        if not project_name == project_selector_text:
            assert_error(error_text=f'Project name: "{CCol.txt_vio(project_name)}" not in project selector, '
                                    f'project selector have: "{CCol.txt_vio(project_selector_text)}"')
