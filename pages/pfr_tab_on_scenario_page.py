from datetime import datetime

from selenium.webdriver.common.keys import Keys

from pages.base_scenario_page import BaseScenarioPage
from pages.site_data.locators import BaseScenarioPageLocators as BSPLocator
from pages.site_data.locators import PFRTabLocators as PFRTPLocator
from pages.site_data.element_texts import PFRTabScenarioPage as PFRTxt


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
        self.find_elem(*PFRTPLocator.TAB_TITLE)
        self.find_elem(*PFRTPLocator.SELECT_GROUP_UPLOAD_FROM_SCENARIO)
        self.find_elem(*PFRTPLocator.DARK_TAB_PFR)
        self.find_elem(*PFRTPLocator.APPLY_BUTTON)
        self.find_elem(*PFRTPLocator.JB_BOTTOM)
        self.find_elem(*PFRTPLocator.BLOCKS_WRAPPER)
        self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE,
                       element_for_format=(PFRTxt.HIERARCHY_LEVEL_BLOCK_NAME[self.language],))
        self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE,
                       element_for_format=(PFRTxt.HIERARCHY_ELEMENTS_BLOCK_NAME[self.language],))
        self.find_elem(*PFRTPLocator.BLOCKS_WITH_TITLE,
                       element_for_format=(PFRTxt.TARGET_VARIABLE_BLOCK_NAME[self.language],))

