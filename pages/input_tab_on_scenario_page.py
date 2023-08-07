from datetime import datetime

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

    def upload_the_file(self, input_file_front_name, file_path):
        self.find_elem(*ITPLocator.SELECT_TYPE_DATA, element_for_format=(input_file_front_name,)).click()
        self.is_clickable(*ITPLocator.select_item('local file')).click()
        self.find_elem(*ITPLocator.UPLOAD_FILE_BUTTON, element_for_format=(input_file_front_name,)).send_keys(file_path)
        self.check_preloader(input_file_front_name, preloader_text='loading')
        self.check_preloader(input_file_front_name, preloader_text='file check')
        self.check_disappeared_preloader(input_file_front_name)

    def file_should_be_uploaded(self, input_file_front_name, system_file_name, check_date=None):
        if check_date is None:
            check_date = datetime.now().strftime("%d.%m.%Y")

        self.check_text_in_info_tag(input_file_front_name, system_file_name)
        self.check_preview_button(input_file_front_name)
        self.check_card_info_text(input_file_front_name)
        self.check_card_info_date(input_file_front_name, check_date)

    def check_text_in_info_tag(self, input_file_front_name, system_file_name):
        tag_text = self.find_elem(*ITPLocator.INFO_TAG_UPLOADED_DATA, element_for_format=(input_file_front_name,)).text
        assert system_file_name == tag_text, \
            f'Uploaded file name "{system_file_name}" not in info tag. Info tag have "{tag_text}"'

    def check_preview_button(self, input_file_front_name, button_text='preview'):
        preview_button_text = self.find_elem(*ITPLocator.PREVIEW_BUTTON, element_for_format=(input_file_front_name,)).text
        assert preview_button_text == button_text, \
            f'Preview button have a text "{preview_button_text}", but should be "{button_text}"'

    def check_card_info_text(self, input_file_front_name, card_info_text='Uploaded on '):
        current_card_info_text = self.find_elem(*ITPLocator.CARD_INFO_TEXT,
                                                element_for_format=(input_file_front_name,)).text
        assert card_info_text in current_card_info_text, \
            f'Card info text: "{current_card_info_text}" don\'t have substring: "{card_info_text}"'

    def check_card_info_date(self, input_file_front_name, check_date):
        current_card_info_text = self.find_elem(*ITPLocator.CARD_INFO_TEXT,
                                                element_for_format=(input_file_front_name,)).text
        assert check_date in current_card_info_text, \
            f'Card info text: "{current_card_info_text}" don\'t have date: "{check_date}"'

    def check_preloader(self, input_file_front_name, preloader_text=None):
        self.find_elem(*ITPLocator.PRELOADER_SPINNER_LARGE, element_for_format=(input_file_front_name,))
        if preloader_text is not None:
            current_preloader_text = self.find_elem(*ITPLocator.PRELOADER_TEXT,
                                                    element_for_format=(input_file_front_name, preloader_text)).text
            assert preloader_text == current_preloader_text, \
                f'Current preloader text: "{current_preloader_text}", but should be "{preloader_text}"'

    def check_disappeared_preloader(self, input_file_front_name):
        assert self.is_disappeared(*ITPLocator.PRELOADER_SPINNER_LARGE, element_for_format=(input_file_front_name,)), \
            'is_disappeared'
