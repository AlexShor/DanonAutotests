from datetime import datetime

from pages.base_scenario_page import BaseScenarioPage
from pages.site_data.default_params import (ProjectType as Ptype,
                                            DefaultInputFilePaths as DIPaths)
from pages.site_data.element_texts import (InputTabScenarioPage as IptTxt,
                                           BaseScenarioPage as BSTxt)
from pages.site_data.locators import (InputTabLocators as ITPLocator,
                                      BasePageLocators as BPLocator)
from pages.site_data.urls import Paths
from input_files.input_data import ScenarioTypes, InputTypeNameMatch
from custom_moduls.console_design.colors import ConsoleColors as CCol


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
        self.find_elem(*ITPLocator.TAB_TITLE, (IptTxt.INPUT_TAB_TITLE[self.language],))
        self.find_elem(*ITPLocator.SELECT_GROUP_UPLOAD_FROM_SCENARIO,
                       (BSTxt.SELECT_GROUP_UPLOAD_FROM_SCENARIO[self.language],))
        self.find_elem(*ITPLocator.CARD)
        self.find_elem(*ITPLocator.DARK_TAB_WITH_NAME, (BSTxt.INPUT_TAB[self.language],))

    def should_be_input_name_in_popover_message_list(self, input_file_front_name):
        self.find_elem(*ITPLocator.MESSAGE_IN_POPOVER_MESSAGE_LIST, (input_file_front_name,))

    # @benchmark
    def should_be_not_input_name_in_popover_message_list(self, input_file_front_name):
        self.is_not_element_present(*ITPLocator.MESSAGE_IN_POPOVER_MESSAGE_LIST, (input_file_front_name,),
                                    timeout=0.5,
                                    error_text=f'Input name: "{CCol.txt_vio(input_file_front_name)}" '
                                               f'is present in popover message list')

    def upload_the_file(self, input_file_front_name,
                        project_type,
                        scenario_type,
                        url_path,
                        optimization_type,
                        file_name,
                        file_path=None,
                        check_preloader=False):
        if file_path is None:
            file_path = DIPaths.PATH[project_type]

        input_type_file_path = self.check_scenario_type_and_open_input_tabs_and_get_file_path(scenario_type,
                                                                                              url_path,
                                                                                              optimization_type)

        if input_type_file_path != '':
            file_path += f'{input_type_file_path}\\'

        self.find_elem(*ITPLocator.SELECT_TYPE_DATA, (input_file_front_name,)).click()
        self.is_clickable(*ITPLocator.ITEM_IN_SELECTOR, (IptTxt.ITEM_IN_SELECTOR_FILE[self.language],),
                          timeout=1).click()
        self.find_elem(*ITPLocator.UPLOAD_FILE_BUTTON, (input_file_front_name,)).send_keys(file_path + file_name)

        if check_preloader:
            self.check_preloader(input_file_front_name, preloader_text=IptTxt.PRELOADER_LOADING[self.language])
            self.check_preloader(input_file_front_name, preloader_text=IptTxt.PRELOADER_CHECK[self.language])
            self.check_disappeared_preloader(input_file_front_name)

    def check_scenario_type_and_open_input_tabs_and_get_file_path(self, scenario_type, url_path, optimization_type):
        input_type_file_path = ''

        if scenario_type == ScenarioTypes.TYPE[Ptype.TETRIS]:

            url_type_md = Paths.URL_PATH_MD
            url_type_sourcing = Paths.URL_PATH_SOURCING
            url_type_industry = Paths.URL_PATH_INDUSTRY
            url_type_milkbalance = Paths.URL_PATH_OPTIMILK

            if url_path == url_type_md:
                self.is_clickable(*ITPLocator.INPUT_TAB_MD, (IptTxt.TETRIS_INPUT_TAB_MD[self.language],)).click()
                self.find_elem(*ITPLocator.ACTIVE_INPUT_TAB_MD, (IptTxt.TETRIS_INPUT_TAB_MD[self.language],))
                input_type_file_path = DIPaths.TETRIS_INPUT_TYPE_FILE_PATH[url_type_md]

            if url_path == url_type_sourcing:
                self.is_clickable(*ITPLocator.INPUT_TAB_SOURCING,
                                  (IptTxt.TETRIS_INPUT_TAB_SOURCING[self.language],)).click()
                self.find_elem(*ITPLocator.ACTIVE_INPUT_TAB_SOURCING,
                               (IptTxt.TETRIS_INPUT_TAB_SOURCING[self.language],))
                input_type_file_path = DIPaths.TETRIS_INPUT_TYPE_FILE_PATH[url_type_sourcing]

            if url_path == url_type_industry:
                self.is_clickable(*ITPLocator.INPUT_TAB_INDUSTRY,
                                  (IptTxt.TETRIS_INPUT_TAB_INDUSTRY[self.language],)).click()
                self.find_elem(*ITPLocator.ACTIVE_INPUT_TAB_INDUSTRY, (IptTxt.TETRIS_INPUT_TAB_INDUSTRY[self.language]))
                input_type_file_path = DIPaths.TETRIS_INPUT_TYPE_FILE_PATH[url_type_industry]

            if url_path == url_type_milkbalance:
                self.is_clickable(*ITPLocator.INPUT_TAB_OPTIMILK,
                                  (IptTxt.TETRIS_INPUT_TAB_OPTIMILK[self.language])).click()
                self.find_elem(*ITPLocator.ACTIVE_INPUT_TAB_OPTIMILK,
                               (IptTxt.TETRIS_INPUT_TAB_OPTIMILK[self.language],))
                input_type_file_path = DIPaths.TETRIS_INPUT_TYPE_FILE_PATH[url_type_milkbalance]

        elif scenario_type == ScenarioTypes.TYPE[Ptype.TETRIS_NEW]:
            optimization_type_sourcing = InputTypeNameMatch.TetrisNew.optimization_type_sourcing
            optimization_type_milk = InputTypeNameMatch.TetrisNew.optimization_type_milk

            if optimization_type == optimization_type_sourcing:
                self.is_clickable(*ITPLocator.INPUT_TAB_SOURCING_LOG,
                                  (IptTxt.TETRIS_NEW_INPUT_TAB_SOURCING[self.language],)).click()
                self.find_elem(*ITPLocator.ACTIVE_INPUT_TAB_SOURCING_LOG,
                               (IptTxt.TETRIS_NEW_INPUT_TAB_SOURCING[self.language],))
                input_type_file_path = DIPaths.TETRIS_NEW_INPUT_TYPE_FILE_PATH[optimization_type_sourcing]

            if optimization_type == optimization_type_milk:
                self.is_clickable(*ITPLocator.INPUT_TAB_MILK,
                                  (IptTxt.TETRIS_NEW_INPUT_TAB_MILK[self.language],)).click()
                self.find_elem(*ITPLocator.ACTIVE_INPUT_TAB_MILK, (IptTxt.TETRIS_NEW_INPUT_TAB_MILK[self.language]))
                input_type_file_path = DIPaths.TETRIS_NEW_INPUT_TYPE_FILE_PATH[optimization_type_milk]

        return input_type_file_path

    def file_should_be_uploaded(self, input_file_front_name, system_file_name, check_date=None, timeout=None):
        if check_date is None:
            check_date = datetime.now().strftime("%d.%m.%Y")

        self.check_text_in_info_tag(input_file_front_name, system_file_name, timeout=timeout)
        self.check_preview_button(input_file_front_name, timeout=timeout)
        self.check_card_info_text(input_file_front_name, timeout=timeout)
        self.check_card_info_date(input_file_front_name, check_date, timeout=timeout)

    def should_be_open_pfr_tab_by_click_on_jenius_button_left(self):
        self.scroll_in_element(*BPLocator.SCROLL_BLOCK, direction='UP')
        self.is_clickable(*ITPLocator.JB_LEFT).click()

    def should_be_open_pfr_tab_by_click_on_jenius_button_bottom(self):
        self.scroll_in_element(*BPLocator.SCROLL_BLOCK, direction='DOWN')
        self.is_clickable(*ITPLocator.JB_BOTTOM).click()

    def should_be_open_pfr_tab_by_click_on_tab_name(self):
        if self.is_element_not_contains_class(*ITPLocator.TAB_WITH_NAME, '_disabled_',
                                              (BSTxt.PFR_TAB[self.language],), timeout=5,
                                              error_text='PFR tab is disabled'):
            self.is_clickable(*ITPLocator.TAB_WITH_NAME, (BSTxt.PFR_TAB[self.language],), timeout=5).click()

    # @benchmark
    def check_text_in_info_tag(self, input_file_front_name, text_in_info_tag, timeout=None):
        tag_text = self.find_elem(*ITPLocator.INFO_TAG_UPLOADED_DATA,
                                  element_for_format=(input_file_front_name,),
                                  timeout=timeout).text
        assert text_in_info_tag == tag_text, \
            f'Text: "{text_in_info_tag}" not in info tag. Info tag have "{tag_text}"'

    # @benchmark
    def check_preview_button(self, input_file_front_name, timeout=None):
        button_text = IptTxt.PREVIEW_BUTTON[self.language]
        preview_button_text = self.find_elem(*ITPLocator.PREVIEW_BUTTON,
                                             element_for_format=(input_file_front_name,),
                                             timeout=timeout).text
        assert preview_button_text == button_text, \
            f'Preview button have a text "{preview_button_text}", but should be "{button_text}"'

    # @benchmark
    def check_card_info_text(self, input_file_front_name,
                             card_info_text=None,
                             timeout=None):
        if card_info_text is None:
            card_info_text = IptTxt.CARD_INFO_UPLOADED[self.language]

        current_card_info_text = self.find_elem(*ITPLocator.CARD_INFO_TEXT,
                                                element_for_format=(input_file_front_name,),
                                                timeout=timeout).text
        assert card_info_text in current_card_info_text, \
            f'Card info text: "{current_card_info_text}" don\'t have substring: "{card_info_text}"'

    # @benchmark
    def check_card_info_date(self, input_file_front_name, check_date, timeout=None):
        current_card_info_text = self.find_elem(*ITPLocator.CARD_INFO_TEXT,
                                                element_for_format=(input_file_front_name,),
                                                timeout=timeout).text
        assert check_date in current_card_info_text, \
            f'Card info text: "{current_card_info_text}" don\'t have date: "{check_date}"'

    # @benchmark
    def check_preloader(self, input_file_front_name, preloader_text=None):
        self.find_elem(*ITPLocator.PRELOADER_SPINNER_LARGE, element_for_format=(input_file_front_name,))
        if preloader_text is not None:
            current_preloader_text = self.find_elem(*ITPLocator.PRELOADER_TEXT,
                                                    element_for_format=(input_file_front_name, preloader_text)).text
            assert preloader_text == current_preloader_text, \
                f'Current preloader text: "{current_preloader_text}", but should be "{preloader_text}"'

    # @benchmark
    def check_disappeared_preloader(self, input_file_front_name, timeout=None):
        self.is_disappeared(*ITPLocator.PRELOADER_SPINNER_LARGE,
                            element_for_format=(input_file_front_name,),
                            timeout=timeout,
                            error_text='Preloader is not disappeared')
