import time
import os

import pytest

from ..pages.base_scenario_page import BaseScenarioPage
from ..pages.scenario_list_page import ScenarioListPage
from ..pages.create_scenario_page import CreateScenarioPage
from ..pages.input_tab_on_scenario_page import InputTabOnScenarioPage
from ..pages.pfr_tab_on_scenario_page import PFRTabOnScenarioPage
from ..pages.login_page import LoginPage
from ..pages.site_data.urls import Links, Pages
from ..input_files.input_data import InputTypeNameMatch
from ..pages.site_data.credentials import Credentials as Creds
from ..conftest import dict_parametrize
from ..pages.site_data.default_params import (ProjectType as Ptype,
                                              ChangeProjectTypeDefaultParams as CPTDP)


project_type = Ptype.RTM


class TestFullSmokePath:
    @pytest.mark.testmark
    def test_user_authorization(self, env, browser):
        link = Links(env).get('LOGIN_PAGE')
        login_page = LoginPage(browser, env, link)
        login_page.open()
        Creds.auth()
        login_page.authorize_user(*Creds.auth().values())

    @pytest.mark.testmark
    def test_user_can_change_project(self, env, browser):
        scenario_list_page = ScenarioListPage(browser, env)
        scenario_list_page.should_be_scenario_list_page()

        scenario_list_page.should_be_sidebar()
        # QA_RTM_Optimizer_1 QA_Promo_optimizer_1 QA_Tetris_Optimizer_2 QA_CFR_Optimizer_2
        scenario_list_page.choose_project(CPTDP.PROJECT_NAME[project_type])

        # Pages.RTM_SCENARIO_LIST PROMO_SCENARIO_LIST TETRIS_SCENARIO_LIST CFR_SCENARIO_LIST
        scenario_list_page.should_be_scenario_list_page(project_url_path=Pages.SCENARIO_LIST[project_type])

    @pytest.mark.testmark
    def test_user_can_open_create_scenario_page(self, env, browser):
        scenario_list_page = ScenarioListPage(browser, env)
        scenario_list_page.should_be_scenario_list_page()
        scenario_list_page.should_be_open_create_scenario_page_by_click_on_jenius_button_bottom()
        # scenario_list_page.should_be_open_create_scenario_page_by_click_on_jenius_button_left()

    #@pytest.mark.testmark
    def test_user_can_create_scenario_and_open_scenario_page(self, env, browser):
        create_scenario_page = CreateScenarioPage(browser, env)
        create_scenario_page.should_be_create_scenario_page()
        # params = {'Name': 'test', 'Group': 'regular scenario', 'Period': '2023 Q4'}
        # params = {'Name': 'test', 'Group': 'Regular', 'Type': 'RTM Optimizer', 'Description': 'test'}
        # params = {'Name': 'test', 'Group': 'Regular', 'Date Bucket': 'RF (Month)', 'Description': 'test', 'Date format': '%yM%m'}
        # params = {'Name': 'test', 'Group': 'Regular', 'Type': 'Optimizer', 'Description': 'test', 'Randomizer regime': 'Demand randomizer'}
        create_scenario_page.create_scenario()

        scenario_page = BaseScenarioPage(browser)
        scenario_page.should_be_scenario_page(project_type=project_type)

    #@pytest.mark.testmark
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

    #@pytest.mark.testmark
    def test_user_can_open_pfr_tab_from_input_tab(self, env, browser):
        input_tab = InputTabOnScenarioPage(browser)
        input_tab.should_be_open_pfr_tab_by_click_on_jenius_button_left()
        
        pfr_tab = PFRTabOnScenarioPage(browser)
        pfr_tab.should_be_pfr_tab_on_scenario_page()

        time.sleep(2)
