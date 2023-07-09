from .base_page import BasePage
from .site_data.locators import ScenarioListPageLocators as SLLocator
from .site_data.locators import BasePageLocators as BPLocator
from ..pages.site_data.urls import Links


class ScenarioListPage(BasePage):
    def should_be_scenario_list_page(self):
        self.find_elem(*BPLocator.HEADER)
        self.find_elem(*SLLocator.BLOCK_FILTERS)
        self.find_elem(*SLLocator.BLOCK_SEARCH)
        assert Links(self.env).get('SCENARIO_LIST_PAGE') == self.browser.current_url, \
            'Current url is not SCENARIO_LIST_PAGE'

    def user_cen_open_create_scenario_page(self):
        self.find_elem(*BPLocator.JB_LEFT).click()
