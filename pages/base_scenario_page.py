from .base_page import BasePage
from .site_data.locators import BaseScenarioPageLocators as BSPLocator
from .site_data.default_params import (CreateScenarioDefaultParams as DefPrm,
                                       ProjectType as Ptype)


class BaseScenarioPage(BasePage):
    def should_be_scenario_page(self, project_type=None):
        self.find_elem(*BSPLocator.SCENARIO_TITLE)
        self.find_elem(*BSPLocator.SCENARIO_SUBTITLE)
        if project_type != Ptype.RTM:
            self.find_elem(*BSPLocator.SELECT_EDIT_ACCESS)
        self.find_elem(*BSPLocator.TAB_INPUT)
        self.find_elem(*BSPLocator.TAB_PFR)
        self.find_elem(*BSPLocator.TAB_OUTPUT)

    def get_scenario_id_from_url(self):
        return self.browser.current_url.split('/')[-1]
