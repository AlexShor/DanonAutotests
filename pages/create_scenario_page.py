import time

from .base_page import BasePage
from .site_data.locators import BasePageLocators as BPLocator
from .site_data.locators import CreateScenarioPageLocators as CSLocator
from .site_data.locators import BaseScenarioPageLocators as BSPLocator
from .site_data.element_texts import CreateScenarioPage as CrtTxt
from ..pages.site_data.urls import Links, Pages


language = 'en'


class CreateScenarioPage(BasePage):
    def should_be_create_scenario_page(self):
        self.is_url_contains('create')
        current_url = self.browser.current_url

        self.find_elem(*CSLocator.INPUT_NAME)
        self.find_elem(*CSLocator.INPUT_DESCRIPTION)
        self.find_elem(*CSLocator.SELECT_GROUP)

        if Pages.PROMO_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.INPUT_GRANULARITY)
            self.find_elem(*CSLocator.SELECT_PERIOD)

        if Pages.RTM_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_TYPE)

        if Pages.TETRIS_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_DATE_BUCKET)
            self.find_elem(*CSLocator.SELECT_DATE_FORMAT)

        if Pages.CFR_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_TYPE)
            self.find_elem(*CSLocator.SELECT_RANDOMIZER_TYPE)

        header = CrtTxt.HEADER[language]
        assert self.find_elem(*CSLocator.HEADER).text == header, \
            f'Current page header is not "{header}"'

    def create_scenario(self, params=None):
        current_url = self.browser.current_url

        name = CrtTxt.INPUT_NAME[language]
        description = CrtTxt.INPUT_DESCRIPTION[language]
        group = CrtTxt.SELECT_GROUP[language]
        period = CrtTxt.SELECT_PERIOD[language]
        _type = CrtTxt.SELECT_TYPE[language]
        date_bucket = CrtTxt.SELECT_DATE_BUCKET[language]
        date_format = CrtTxt.SELECT_DATE_FORMAT[language]
        randomizer_type = CrtTxt.SELECT_RANDOMIZER_TYPE[language]

        if params.get(name) is not None:
            input_name = self.find_elem(*CSLocator.INPUT_NAME)
            input_name.send_keys(u'\ue009' + u'\ue003')
            input_name.send_keys(params[name])

        if params.get(description) is not None:
            self.find_elem(*CSLocator.INPUT_DESCRIPTION).send_keys(params[description])

        self.find_elem(*CSLocator.SELECT_GROUP).click()
        self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(group),)).click()

        if Pages.PROMO_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_PERIOD).click()
            self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(period),)).click()

        if Pages.RTM_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_TYPE).click()
            self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(_type),)).click()

        if Pages.TETRIS_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_DATE_BUCKET).click()
            self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(date_bucket),)).click()

            self.find_elem(*CSLocator.SELECT_DATE_FORMAT).click()
            self.find_elem(*CSLocator.SELECT_DATE_FORMAT).click()
            self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(date_format),)).click()

        if Pages.CFR_CREATE_SCENARIO in current_url:
            self.find_elem(*CSLocator.SELECT_TYPE).click()
            self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(_type),)).click()

            self.find_elem(*CSLocator.SELECT_RANDOMIZER_TYPE).click()
            self.is_clickable(*CSLocator.ITEM_IN_SELECTOR, element_for_format=(params.get(randomizer_type),)).click()

        self.find_elem(*BPLocator.JENIUS_BUTTON).click()

        self.find_elem(*BSPLocator.SCENARIO_TITLE)


