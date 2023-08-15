import time

from pages.base_page import BasePage
from pages.site_data.locators import (BasePageLocators as BPLocator,
                                      ScenarioListPageLocators as SLLocator)
from pages.site_data.urls import Links


class ScenarioListPage(BasePage):
    def should_be_scenario_list_page(self, project_url_path=None):
        self.find_elem(*BPLocator.HEADER)
        self.find_elem(*SLLocator.BLOCK_FILTERS)
        self.find_elem(*SLLocator.BLOCK_SEARCH)

        if project_url_path is not None:
            assert self.is_url_contains(project_url_path), f'Current url is not contains: "{project_url_path}"'

    def should_be_open_create_scenario_page_by_click_on_jenius_button_left(self):
        self.scroll_in_element(*BPLocator.SCROLL_BLOCK, direction='UP')
        self.is_clickable(*BPLocator.JB_LEFT).click()

    def should_be_open_create_scenario_page_by_click_on_jenius_button_bottom(self):
        self.is_element_scroll_height(*BPLocator.SCROLL_BLOCK,
                                      expected_scroll_height=self.browser.get_window_size()['height'])

        self.scroll_in_element(*BPLocator.SCROLL_BLOCK, direction='DOWN')
        self.is_clickable(*BPLocator.JB_BOTTOM).click()

    def user_can_open_scenario_page_by_click_on_scenario_title(self, scenario_title):
        self.find_elem(*SLLocator.SCENARIO_TITLE, element_for_format=(scenario_title, )).click()
