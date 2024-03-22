import inspect
import time

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.site_data.locators import (BasePageLocators as BPLocator,
                                      PFRTabLocators as PFRTPLocator)

from custom_moduls import custom_expected_conditions as CEC
from custom_moduls.console_design.colors import ConsoleColors as CCol
from custom_moduls.console_design.link_to_modules import print_link_to_modules as print_link
from pages.site_data.element_texts import BasePage as BPTxt


def assert_error(error_text, method=None, css_selector=''):

    f_back = inspect.currentframe().f_back.f_back
    link = print_link(file=f_back.f_code.co_filename, line=f_back.f_lineno)
    code_obj_name = f_back.f_code.co_name
    print_text_error = f'\r{link}[{CCol.txt_blu(code_obj_name)}] '

    if error_text:
        print_text_error += error_text
    else:
        print_text_error += f'No Such Element by {CCol.txt_yel(method)}: "{CCol.txt_vio(css_selector)}"'
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

    def find_elem(self, method, css_selector, element_for_format=(), error_text='',
                  elem_id: int | None = 0, timeout=None):

        css_selector = css_selector.format(*element_for_format)

        if timeout is not None:
            self.browser.implicitly_wait(timeout)
        found_elements = self.browser.find_elements(method, css_selector)
        self.browser.implicitly_wait(self.implicitly_wait_timeout)

        if len(found_elements) == 0:
            assert_error(error_text, method=method, css_selector=css_selector)

        return found_elements if elem_id is None else found_elements[elem_id]

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

        css_selector = css_selector.format(*element_for_format)

        try:
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until(EC.element_to_be_clickable((method, css_selector)))
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=f'Element is not clickable: "{CCol.txt_vio(css_selector)}"')
            else:
                return False
        # except ElementClickInterceptedException:
        #     element = self.find_elem(method, css_selector, element_for_format, timeout=timeout)
        #     self.browser.execute_script("arguments[0].click();", element)

        return self.find_elem(method, css_selector, element_for_format, timeout=timeout)

    def is_element_scroll_height(self, method, css_selector, expected_scroll_height,
                                 element_for_format=(), error_text='', timeout=4):

        css_selector = css_selector.format(*element_for_format)

        try:
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until(CEC.element_has_scroll_size(css_selector, expected_scroll_height))
        except TimeoutException:
            if error_text == '':
                error_text = (f'Scroll height by element: "{CCol.txt_vio(css_selector)}" '
                              f'lower then expected scroll height: "{CCol.txt_vio(expected_scroll_height)}"')
            assert_error(error_text=error_text)
        return True

    def is_element_not_contains_class(self, method, css_selector, class_name, element_for_format=(),
                                      error_text='', timeout=4, return_bool=False):

        css_selector = css_selector.format(*element_for_format)

        try:
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until_not(CEC.element_has_css_class(method, css_selector, class_name))
        except TimeoutException:

            if not return_bool:
                assert_error(error_text=error_text)
            else:
                return False

        return True

    def is_not_element_present(self, method, css_selector, element_for_format=(),
                               error_text='', timeout=4, return_bool=False):

        css_selector = css_selector.format(*element_for_format)

        try:
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until(EC.presence_of_element_located((method, css_selector)))
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
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until_not(EC.text_to_be_present_in_element((method, css_selector), text))
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=error_text)
            else:
                return False
        return True

    def is_disappeared(self, method, css_selector, element_for_format=(), error_text='', timeout=4, return_bool=False):

        css_selector = css_selector.format(*element_for_format)

        try:
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until_not(EC.visibility_of_element_located((method, css_selector)))
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=error_text)
            else:
                return False
        return True

    def is_url_contains(self, text_from_url, error_text='', timeout=4, return_bool=False):
        try:
            wait = WebDriverWait(self.browser, timeout=timeout)
            wait.until(EC.url_contains(text_from_url))
        except TimeoutException:
            if not return_bool:
                assert_error(error_text=error_text)
            else:
                return False
        return True

    def should_be_sidebar(self):
        self.find_elem(*BPLocator.SIDEBAR)
        self.find_elem(*BPLocator.PROJECT_SELECTOR)
        self.find_elem(*BPLocator.ALL_SCENARIOS_BUTTON, (BPTxt.ALL_SCENARIOS_BUTTON[self.language], ))
        self.find_elem(*BPLocator.OPEN_MENU_BUTTON)

    def choose_project(self, project_name):
        self.find_elem(*BPLocator.PROJECT_SELECTOR).click()
        self.is_clickable(*BPLocator.ITEM_IN_SELECTOR, element_for_format=(project_name,)).click()

        project_selector_text = self.find_elem(*BPLocator.PROJECT_SELECTOR).text
        if not project_name == project_selector_text:
            assert_error(error_text=f'Project name: "{CCol.txt_vio(project_name)}" not in project selector, '
                                    f'project selector have: "{CCol.txt_vio(project_selector_text)}"')

    def choose_data_in_multiple_select(self, tree_elements=None, timeout=0.3):
        if tree_elements is None:
            tree_elements = ['Select all']

        virtual_list_items = self.find_elem(*PFRTPLocator.SELECT_VIRTUAL_LIST_ITEM, elem_id=None)

        def find_and_click(list_items, item_name):
            for i in range(len(list_items)):
                if list_items[i].text == item_name:
                    time.sleep(timeout)
                    list_items[i].click()
                    return list_items[i:]

        for element in tree_elements:
            virtual_list_items = find_and_click(virtual_list_items, element)

    def search_data_in_multiple_select(self, method, css_selector, tree_elements=None, timeout=0.3):
        if tree_elements is None:
            tree_elements = ['Select all']

        virtual_list_items = self.find_elem(method, css_selector, elem_id=None)