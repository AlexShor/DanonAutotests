from .base_page import BasePage
from .site_data.locators import BaseScenarioPageLocators as BSPLocator


class BaseScenarioPage(BasePage):
    def should_be_scenario_page(self):
        self.find_elem(*BSPLocator.SCENARIO_TITLE)
        self.find_elem(*BSPLocator.SCENARIO_SUBTITLE)
        self.find_elem(*BSPLocator.SELECT_EDIT_ACCESS)
        self.find_elem(*BSPLocator.TAB_INPUT)
        self.find_elem(*BSPLocator.TAB_PFR)
        self.find_elem(*BSPLocator.TAB_OUTPUT)
