from datetime import datetime

from selenium.webdriver.common.keys import Keys

from .base_scenario_page import BaseScenarioPage
from .site_data.locators import BaseScenarioPageLocators as BSPLocator
from .site_data.locators import InputTabLocators as ITPLocator


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, time.time() - t)
        return res
    return wrapper


class InputTabOnScenarioPage(BaseScenarioPage):
    def should_be_input_tab_on_scenario_page(self):
        self.find_elem(*ITPLocator.TAB_TITLE)
        self.find_elem(*ITPLocator.SELECT_GROUP_UPLOAD_FROM_SCENARIO)
        self.find_elem(*ITPLocator.CARD)
        self.find_elem(*ITPLocator.DARK_TAB_INPUT)

    def should_be_input_name_in_popover_message_list(self, input_file_front_name):
        self.find_elem(*ITPLocator.MESSAGE_IN_POPOVER_MESSAGE_LIST, element_for_format=(input_file_front_name,))

    #@benchmark
    def should_be_not_input_name_in_popover_message_list(self, input_file_front_name):
        assert self.is_not_element_present(*ITPLocator.MESSAGE_IN_POPOVER_MESSAGE_LIST,
                                           element_for_format=(input_file_front_name,),
                                           timeout=0.5), \
            f'Input name: "{input_file_front_name}" is present in popover message list'

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

    def should_be_open_pfr_tab_by_click_on_jenius_button_left(self):
        self.find_elem(*ITPLocator.HTML_TAG).send_keys(Keys.HOME)
        self.is_clickable(*ITPLocator.JB_LEFT).click()

    def should_be_open_pfr_tab_by_click_on_jenius_button_bottom(self):
        self.find_elem(*ITPLocator.HTML_TAG).send_keys(Keys.END)
        self.is_clickable(*ITPLocator.JB_BOTTOM).click()

    #@benchmark
    def check_text_in_info_tag(self, input_file_front_name, text_in_info_tag):
        tag_text = self.find_elem(*ITPLocator.INFO_TAG_UPLOADED_DATA, element_for_format=(input_file_front_name,)).text
        assert text_in_info_tag == tag_text, \
            f'Text: "{text_in_info_tag}" not in info tag. Info tag have "{tag_text}"'

    #@benchmark
    def check_preview_button(self, input_file_front_name, button_text='preview'):
        preview_button_text = self.find_elem(*ITPLocator.PREVIEW_BUTTON, element_for_format=(input_file_front_name,)).text
        assert preview_button_text == button_text, \
            f'Preview button have a text "{preview_button_text}", but should be "{button_text}"'

    #@benchmark
    def check_card_info_text(self, input_file_front_name, card_info_text='Uploaded on '):
        current_card_info_text = self.find_elem(*ITPLocator.CARD_INFO_TEXT,
                                                element_for_format=(input_file_front_name,)).text
        assert card_info_text in current_card_info_text, \
            f'Card info text: "{current_card_info_text}" don\'t have substring: "{card_info_text}"'

    #@benchmark
    def check_card_info_date(self, input_file_front_name, check_date):
        current_card_info_text = self.find_elem(*ITPLocator.CARD_INFO_TEXT,
                                                element_for_format=(input_file_front_name,)).text
        assert check_date in current_card_info_text, \
            f'Card info text: "{current_card_info_text}" don\'t have date: "{check_date}"'

    #@benchmark
    def check_preloader(self, input_file_front_name, preloader_text=None):
        self.find_elem(*ITPLocator.PRELOADER_SPINNER_LARGE, element_for_format=(input_file_front_name,))
        if preloader_text is not None:
            current_preloader_text = self.find_elem(*ITPLocator.PRELOADER_TEXT,
                                                    element_for_format=(input_file_front_name, preloader_text)).text
            assert preloader_text == current_preloader_text, \
                f'Current preloader text: "{current_preloader_text}", but should be "{preloader_text}"'

    #@benchmark
    def check_disappeared_preloader(self, input_file_front_name):
        assert self.is_disappeared(*ITPLocator.PRELOADER_SPINNER_LARGE, element_for_format=(input_file_front_name,)), \
            'Preloader is not disappeared'
