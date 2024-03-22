from datetime import datetime
import time

from selenium.webdriver.common.keys import Keys

from pages.base_scenario_page import BaseScenarioPage
from pages.site_data.locators import BaseScenarioPageLocators as BSPLocator
from pages.site_data.locators import PFRTabLocators as PFRTPLocator
from pages.site_data.element_texts import (PFRTabScenarioPage as PFRTxt,
                                           BaseScenarioPage as BSTxt)
from pages.pfr_tab_on_scenario_page.base_pfr_tab_on_scenario_page import BasePFRTabOnScenarioPage


class PromoPFRTabOnScenarioPage(BasePFRTabOnScenarioPage):
    def should_be_pfr_tab_on_scenario_page(self):
        self.base_should_be_pfr_tab_on_scenario_page()
        self.should_be_select_group_upload_from_scenario_and_apply_button()

        titles = [PFRTxt.HIERARCHY_LEVEL_BLOCK_NAME[self.language],
                  PFRTxt.HIERARCHY_ELEMENTS_BLOCK_NAME[self.language],
                  PFRTxt.TARGET_VARIABLE_BLOCK_NAME[self.language]]
        self.should_be_blocks_with_title(titles)

    def choose_hierarchy_levels(self, radio_group_title, radio_button_title):
        radio_button_data = (PFRTxt.HIERARCHY_LEVEL_BLOCK_NAME[self.language], radio_group_title, radio_button_title)

        self.find_elem(*PFRTPLocator.RADIO_BUTTON, radio_button_data).click()
        self.is_element_contains_text(*PFRTPLocator.RADIO_BUTTONS_CHECKED, radio_button_data[:2],
                                      text=radio_button_title)

    def choose_data_in_hierarchy_elements_select(self, select_name, tree_elements=None):
        self.find_elem(*PFRTPLocator.SELECT_IN_BLOCKS_WITH_TITLE,
                       (PFRTxt.HIERARCHY_ELEMENTS_BLOCK_NAME[self.language],
                        select_name, )).click()
        time.sleep(0.5)
        self.choose_data_in_multiple_select(tree_elements)

    def search_data_in_hierarchy_elements_select(self, select_name, text):
        self.find_elem(*PFRTPLocator.SELECT_IN_BLOCKS_WITH_TITLE,
                       (PFRTxt.HIERARCHY_ELEMENTS_BLOCK_NAME[self.language],
                        select_name,)).click()
        time.sleep(0.5)
        self.find_elem(*PFRTPLocator.INPUT_IN_MULTIPLE_SELECT).send_keys(text)

    def choose_data_in_target_variable_select(self, select_name, data):
        self.find_elem(*PFRTPLocator.SELECT_IN_BLOCKS_WITH_TITLE,
                       (PFRTxt.TARGET_VARIABLE_BLOCK_NAME[self.language],
                        select_name,)).click()
        self.is_clickable(*PFRTPLocator.ITEM_IN_SELECTOR, (data,)).click()

    def input_data_in_target_variable_input(self, input_name, text):
        elem = self.find_elem(*PFRTPLocator.INPUT_IN_BLOCKS_WITH_TITLE,
                       (PFRTxt.TARGET_VARIABLE_BLOCK_NAME[self.language],
                        input_name,))#.send_keys(text)
        self.browser.execute_script(f"arguments[0].setAttribute('value', '{text}');", elem)
