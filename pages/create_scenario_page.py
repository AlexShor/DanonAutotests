import time

from pages.base_page import BasePage
from pages.site_data.locators import BasePageLocators as BPLocator
from pages.site_data.locators import CreateScenarioPageLocators as CSLocator
from pages.site_data.locators import BaseScenarioPageLocators as BSPLocator
from pages.site_data.element_texts import CreateScenarioPage as CrtTxt
from pages.site_data.urls import Links, Pages
from pages.site_data.default_params import (CreateScenarioDefaultParams as DefPrm,
                                            ProjectType as Ptype)
from custom_moduls.console_design.colors import ConsoleColors as CCol


class CreateScenarioPage(BasePage):
    def should_be_create_scenario_page(self):
        text_from_url = 'create'
        self.is_url_contains(text_from_url=text_from_url,
                             error_text=f'Current url is not contains: "{CCol.txt_vio(text_from_url)}"')
        current_url = self.browser.current_url

        self.find_elem(*CSLocator.INPUT_NAME, (CrtTxt.INPUT_NAME[self.language], ))
        self.find_elem(*CSLocator.INPUT_DESCRIPTION, (CrtTxt.INPUT_DESCRIPTION[self.language], ))
        self.find_elem(*CSLocator.SELECT_GROUP, (CrtTxt.SELECT_GROUP[self.language], ))

        if Pages.SCENARIO_LIST[Ptype.PROMO] in current_url:
            self.find_elem(*CSLocator.INPUT_GRANULARITY, (CrtTxt.INPUT_GRANULARITY[self.language], ))
            self.find_elem(*CSLocator.SELECT_PERIOD, (CrtTxt.SELECT_PERIOD[self.language], ))

        if Pages.SCENARIO_LIST[Ptype.RTM] in current_url:
            self.find_elem(*CSLocator.SELECT_TYPE, (CrtTxt.SELECT_TYPE[self.language], ))

        if Pages.SCENARIO_LIST[Ptype.TETRIS] in current_url:
            self.find_elem(*CSLocator.SELECT_DATE_BUCKET, (CrtTxt.SELECT_DATE_BUCKET[self.language], ))
            self.find_elem(*CSLocator.SELECT_DATE_FORMAT, (CrtTxt.SELECT_DATE_FORMAT[self.language], ))

        if Pages.SCENARIO_LIST[Ptype.CFR] in current_url:
            self.find_elem(*CSLocator.SELECT_TYPE, (CrtTxt.SELECT_TYPE[self.language], ))
            self.find_elem(*CSLocator.SELECT_RANDOMIZER_TYPE, (CrtTxt.SELECT_RANDOMIZER_TYPE[self.language], ))

        header = CrtTxt.HEADER[self.language]
        assert self.find_elem(*CSLocator.HEADER).text == header, \
            f'Current page header is not "{header}"'

    def create_scenario(self, params=None):
        if params is None:
            params = {}
        current_url = self.browser.current_url

        name = CrtTxt.INPUT_NAME[self.language]
        description = CrtTxt.INPUT_DESCRIPTION[self.language]
        group = CrtTxt.SELECT_GROUP[self.language]
        period = CrtTxt.SELECT_PERIOD[self.language]
        _type = CrtTxt.SELECT_TYPE[self.language]
        date_bucket = CrtTxt.SELECT_DATE_BUCKET[self.language]
        date_format = CrtTxt.SELECT_DATE_FORMAT[self.language]
        randomizer_type = CrtTxt.SELECT_RANDOMIZER_TYPE[self.language]
        module_sourcing = CrtTxt.CHECK_BOX_SOURCING[self.language]
        module_milk = CrtTxt.CHECK_BOX_MILK[self.language]

        if params.get(name) is not None:
            input_name = self.find_elem(*CSLocator.INPUT_NAME, (CrtTxt.INPUT_NAME[self.language], ))
            input_name.send_keys(u'\ue009' + u'\ue003')
            input_name.send_keys(params[name])

        if params.get(description) is not None:
            self.find_elem(*CSLocator.INPUT_DESCRIPTION,
                           (CrtTxt.INPUT_DESCRIPTION[self.language], )).send_keys(params[description])

        if Pages.CREATE_SCENARIO[Ptype.PROMO] in current_url:
            self.choose_promo_params(params, period, group)

        if Pages.CREATE_SCENARIO[Ptype.RTM] in current_url:
            self.choose_rtm_params(params, _type, group)

        # if Pages.CREATE_SCENARIO[Ptype.TETRIS] in current_url:
        #     self.choose_tetris_params(params, date_bucket, date_format, group)

        if Pages.CREATE_SCENARIO[Ptype.TETRIS_NEW] in current_url:
            self.choose_tetris_new_params(params, group, module_sourcing, module_milk)

        if Pages.CREATE_SCENARIO[Ptype.CFR] in current_url:
            self.choose_cfr_params(params, _type, randomizer_type, group)

        self.find_elem(*BPLocator.JENIUS_BUTTON).click()
        self.find_elem(*BSPLocator.SCENARIO_TITLE)

    def choose_promo_params(self, params, period, group):
        self.find_elem(*CSLocator.SELECT_PERIOD, (CrtTxt.SELECT_PERIOD[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(period, DefPrm.PROMO_PARAMS[period]),)).click()

        self.find_elem(*CSLocator.SELECT_GROUP, (CrtTxt.SELECT_GROUP[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(group, DefPrm.PROMO_PARAMS[group]),)).click()

    def choose_rtm_params(self, params, _type, group):
        self.find_elem(*CSLocator.SELECT_TYPE, (CrtTxt.SELECT_TYPE[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(_type, DefPrm.RTM_PARAMS[_type]),)).click()

        self.find_elem(*CSLocator.SELECT_GROUP, (CrtTxt.SELECT_GROUP[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(group, DefPrm.RTM_PARAMS[group]),)).click()

    def choose_tetris_params(self, params, date_bucket, date_format, group):
        self.find_elem(*CSLocator.SELECT_DATE_BUCKET, (CrtTxt.SELECT_DATE_BUCKET[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR,
                          (params.get(date_bucket, DefPrm.TETRIS_PARAMS[date_bucket]),)).click()

        self.find_elem(*CSLocator.SELECT_DATE_FORMAT, (CrtTxt.SELECT_DATE_FORMAT[self.language], )).click()
        self.find_elem(*CSLocator.SELECT_DATE_FORMAT, (CrtTxt.SELECT_DATE_FORMAT[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR,
                          (params.get(date_format, DefPrm.TETRIS_PARAMS[date_format]),)).click()

        self.find_elem(*CSLocator.SELECT_GROUP, (CrtTxt.SELECT_GROUP[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(group, DefPrm.TETRIS_PARAMS[group]),)).click()

    def choose_tetris_new_params(self, params, group, module_sourcing, module_milk):
        self.find_elem(*CSLocator.SELECT_GROUP, (CrtTxt.SELECT_GROUP[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(group, DefPrm.TETRIS_NEW_PARAMS[group]),)).click()

        if module_sourcing:
            self.find_elem(*CSLocator.CHECK_BOX_SOURCING, (CrtTxt.CHECK_BOX_SOURCING[self.language], )).click()
            self.find_elem(*CSLocator.CHECK_BOX_SOURCING_CHECKED, (CrtTxt.CHECK_BOX_SOURCING[self.language], ))
        if module_milk:
            self.find_elem(*CSLocator.CHECK_BOX_MILK, (CrtTxt.CHECK_BOX_MILK[self.language], )).click()
            self.find_elem(*CSLocator.CHECK_BOX_MILK_CHECKED, (CrtTxt.CHECK_BOX_MILK[self.language], ))



        # self.is_element_contains_text(*CSLocator.SELECT_GROUP, text=params.get(group, DefPrm.TETRIS_NEW_PARAMS[group]))

    def choose_cfr_params(self, params, _type, randomizer_type, group):
        self.find_elem(*CSLocator.SELECT_TYPE, (CrtTxt.SELECT_TYPE[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(_type, DefPrm.CFR_PARAMS[_type]),)).click()

        self.find_elem(*CSLocator.SELECT_RANDOMIZER_TYPE, (CrtTxt.SELECT_RANDOMIZER_TYPE[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR,
                          (params.get(randomizer_type, DefPrm.CFR_PARAMS[randomizer_type]),)).click()

        self.find_elem(*CSLocator.SELECT_GROUP, (CrtTxt.SELECT_GROUP[self.language], )).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, (params.get(group, DefPrm.CFR_PARAMS[group]),)).click()
