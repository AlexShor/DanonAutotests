import time
import os

import pytest

from ..pages.base_scenario_page import BaseScenarioPage
from ..pages.scenario_list_page import ScenarioListPage
from ..pages.create_scenario_page import CreateScenarioPage
from ..pages.input_tab_on_scenario_page import InputTabOnScenarioPage
from ..pages.login_page import LoginPage
from ..pages.site_data.urls import Links
from ..input_files.input_data import InputTypeNameMatch
from ..pages.site_data.credentials import Credentials as Creds
from ..conftest import dict_parametrize


class TestStart:
    def test_user_authorization(self, env, browser):
        link = Links(env).get('LOGIN_PAGE')
        login_page = LoginPage(browser, env, link)
        login_page.open()
        Creds.auth()
        login_page.authorize_user(*Creds.auth().values())

    def test_user_can_open_create_scenario_page(self, env, browser):
        link = Links(env).get('SCENARIO_LIST_PAGE')
        scenario_list_page = ScenarioListPage(browser, env, link)
        scenario_list_page.should_be_scenario_list_page()
        scenario_list_page.user_can_open_create_scenario_page()

    def test_user_can_create_scenario_and_open_scenario_page(self, env, browser):
        link = Links(env).get('PROMO_CREATE_SCENARIO')
        create_scenario_page = CreateScenarioPage(browser, env, link)
        create_scenario_page.should_be_create_scenario_page()
        create_scenario_page.create_scenario(name='test',
                                             description='',
                                             group='regular scenario',
                                             period='2023 Q4')
        scenario_page = BaseScenarioPage(browser)
        scenario_page.should_be_scenario_page()

    @dict_parametrize(InputTypeNameMatch.Promo.TYPES)
    def test_user_can_add_input_file(self, env, browser,
                                     type_scenarios,
                                     url_path,
                                     system_file_name,
                                     front_name):
        input_tab = InputTabOnScenarioPage(browser)
        input_tab.should_be_input_tab_on_scenario_page()

        input_tab.should_be_input_name_in_popover_message_list(front_name)

        path = '\\input_files\\files\\promo\\input_files\\'
        path = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1]) + path
        file_path = path + f'{system_file_name}.csv'
        input_tab.upload_the_file(front_name, file_path)

        input_tab.file_should_be_uploaded(front_name, system_file_name=f'{system_file_name}.csv')
        input_tab.should_be_not_input_name_in_popover_message_list(front_name)

    def test_user_can_open_pfr_tab_from_input_tab(self, env, browser):
        input_tab = InputTabOnScenarioPage(browser)
        input_tab.should_be_open_pfr_tab_by_click_on_jenius_button_left()
        

        time.sleep(2)
