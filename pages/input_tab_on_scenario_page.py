from .base_scenario_page import BaseScenarioPage
from .site_data.locators import BaseScenarioPageLocators as BSPLocator
from .site_data.locators import InputTabLocators as ITPLocator


class InputTabOnScenarioPage(BaseScenarioPage):
    def should_be_scenario_page(self):
        self.find_elem(*BSPLocator.SCENARIO_TITLE)
        self.find_elem(*BSPLocator.SCENARIO_SUBTITLE)
        self.find_elem(*BSPLocator.SELECT_EDIT_ACCESS)
        self.find_elem(*BSPLocator.TAB_INPUT)
        self.find_elem(*BSPLocator.TAB_PFR)
        self.find_elem(*BSPLocator.TAB_OUTPUT)

    def upload_the_file(self, input_name, file_path):
        self.find_elem(*ITPLocator.SELECT_TYPE_DATA, element_for_format=input_name).click()
        self.is_clickable(*ITPLocator.select_item('local file')).click()
        self.find_elem(*ITPLocator.UPLOAD_FILE_BUTTON, element_for_format=input_name).send_keys(file_path)

