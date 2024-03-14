from datetime import datetime

from selenium.webdriver.common.keys import Keys

from pages.base_scenario_page import BaseScenarioPage
from pages.site_data.locators import BaseScenarioPageLocators as BSPLocator
from pages.site_data.locators import PFRTabLocators as PFRTPLocator
from pages.site_data.element_texts import (PFRTabScenarioPage as PFRTxt,
                                           BaseScenarioPage as BSTxt)


# language = 'en'


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, time.time() - t)
        return res

    return wrapper


class PFRTabOnScenarioPage(BaseScenarioPage):
    def should_be_pfr_tab_on_scenario_page(self):
        self.find_elem(*PFRTPLocator.TAB_TITLE, (PFRTxt.PFR_TAB_TITLE[self.language], ))
        self.find_elem(*PFRTPLocator.SELECT_GROUP_UPLOAD_FROM_SCENARIO,
                       (BSTxt.SELECT_GROUP_UPLOAD_FROM_SCENARIO[self.language],))
        self.find_elem(*PFRTPLocator.DARK_TAB_PFR, (BSTxt.PFR_TAB[self.language],))
        self.find_elem(*PFRTPLocator.APPLY_BUTTON)
        self.find_elem(*PFRTPLocator.JB_BOTTOM)
        self.find_elem(*PFRTPLocator.BLOCKS_WRAPPER)
        self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE, (PFRTxt.HIERARCHY_LEVEL_BLOCK_NAME[self.language],))
        self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE, (PFRTxt.HIERARCHY_ELEMENTS_BLOCK_NAME[self.language],))
        self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE, (PFRTxt.TARGET_VARIABLE_BLOCK_NAME[self.language],))


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

    def choose_data_in_select_customers(self):
        self.find_elem(*PFRTPLocator.SELECT_IN_BLOCKS_WITH_TITLE, (PFRTxt.HIERARCHY_ELEMENTS_BLOCK_NAME[self.language],
                                                                   'select customers', )).click()

class RtmPFRTabOnScenarioPage(BasePFRTabOnScenarioPage):
    pass


class CfrPFRTabOnScenarioPage(BasePFRTabOnScenarioPage):
    pass


class TetrisPFRTabOnScenarioPage(BasePFRTabOnScenarioPage):
    pass
