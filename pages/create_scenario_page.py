from .base_page import BasePage
from .site_data.locators import BasePageLocators as BPLocator
from .site_data.locators import CreateScenarioPageLocators as CSLocator
from .site_data.locators import BaseScenarioPageLocators as BSPLocator
from ..pages.site_data.urls import Links


class CreateScenarioPage(BasePage):
    def should_be_create_scenario_page(self):
        self.find_elem(*CSLocator.INPUT_NAME)
        self.find_elem(*CSLocator.INPUT_DESCRIPTION)
        self.find_elem(*CSLocator.INPUT_GRANULARITY)
        self.find_elem(*CSLocator.SELECT_GROUP)
        self.find_elem(*CSLocator.SELECT_PERIOD)
        assert self.find_elem(*CSLocator.HEADER).text == 'New scenario', 'Current header is not "New scenario"'
        assert Links(self.env).get('CREATE_SCENARIO_PAGE') == self.browser.current_url, \
            'Current url is not PROMO_CREATE_SCENARIO'

    def create_scenario(self, name='', description='', group='', period=''):
        if name:
            input_name = self.find_elem(*CSLocator.INPUT_NAME)
            input_name.send_keys(u'\ue009' + u'\ue003')
            input_name.send_keys(name)

        self.find_elem(*CSLocator.INPUT_DESCRIPTION).send_keys(description)

        self.find_elem(*CSLocator.SELECT_GROUP).click()
        self.is_clickable(*CSLocator.select_item(group)).click()

        self.find_elem(*CSLocator.SELECT_PERIOD).click()
        self.is_clickable(*CSLocator.select_item(period)).click()

        self.find_elem(*BPLocator.JENIUS_BUTTON).click()

        self.find_elem(*BSPLocator.SCENARIO_TITLE)

    def get_scenario_id_from_url(self):
        return self.browser.current_url.split('/')[-1]
