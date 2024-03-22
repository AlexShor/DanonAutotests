from datetime import datetime
import time

from selenium.webdriver.common.keys import Keys

from pages.base_scenario_page import BaseScenarioPage
from pages.site_data.locators import BaseScenarioPageLocators as BSPLocator
from pages.site_data.locators import PFRTabLocators as PFRTPLocator
from pages.site_data.element_texts import (PFRTabScenarioPage as PFRTxt,
                                           BaseScenarioPage as BSTxt)


class BasePFRTabOnScenarioPage(BaseScenarioPage):
    def __init__(self, browser, env='', url='', timeout=10, language='en'):
        super().__init__(browser, env, url, timeout, language)

    def base_should_be_pfr_tab_on_scenario_page(self):
        self.find_elem(*PFRTPLocator.TAB_TITLE, (PFRTxt.PFR_TAB_TITLE[self.language]))

    def should_be_select_group_upload_from_scenario_and_apply_button(self):
        self.find_elem(*PFRTPLocator.SELECT_GROUP_UPLOAD_FROM_SCENARIO,
                       (BSTxt.SELECT_GROUP_UPLOAD_FROM_SCENARIO[self.language],))
        self.find_elem(*PFRTPLocator.APPLY_BUTTON)

    def should_be_blocks_with_title(self, block_titles: list):
        for block_title in block_titles:
            self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE, (block_title,))
