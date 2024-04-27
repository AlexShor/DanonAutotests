import time

import pytest

from custom_moduls.custom_parametrize import custom_parametrize
from input_files.input_data import InputTypeNameMatch
from pages.base_scenario_page import BaseScenarioPage
from pages.create_scenario_page import CreateScenarioPage
from pages.input_tab_on_scenario_page import InputTabOnScenarioPage
from pages.login_page import LoginPage
from pages.pfr_tab_on_scenario_page.promo_pfr_tab_on_scenario_page import PromoPFRTabOnScenarioPage
from pages.scenario_list_page import ScenarioListPage
from pages.site_data.credentials import Credentials as Creds
from pages.site_data.default_params import (ProjectType as Ptype,
                                            DefaultProjectNames as DPNames,
                                            DefaultProjectLanguage as DPLang)
from pages.site_data.urls import Links, Pages


project_type = Ptype.PROMO
scenario_id = None
scenario_title = None
types = {Ptype.PROMO: InputTypeNameMatch.Promo.TYPES,
         Ptype.RTM: InputTypeNameMatch.RTM.TYPES,
         Ptype.TETRIS: InputTypeNameMatch.Tetris.TYPES,
         Ptype.TETRIS_NEW: InputTypeNameMatch.TetrisNew.TYPES,
         Ptype.CFR: InputTypeNameMatch.CFR.TYPES}[project_type]

skip = {Ptype.PROMO: {},
        Ptype.RTM: {},
        Ptype.TETRIS: {'bom': {'method': 'skipif', 'msg': 'Input is not agreed and not finalized'},
                       'stop_buyers': {'method': 'xfail', 'msg': 'Bug'}},
        Ptype.TETRIS_NEW: {},
        Ptype.CFR: {}}[project_type]

language = DPLang.TYPE[project_type]


class TestFullSmokePath:
    @pytest.mark.test_full_smoke
    @pytest.mark.fast_test
    @pytest.mark.select_test
    # @pytest.mark.incremental
    def test_user_authorization(self, env, browser):
        link = Links(env).get('LOGIN_PAGE')
        login_page = LoginPage(browser, env, link)
        login_page.open()
        login_page.authorize_user(*Creds.auth(env).values())

        scenario_list_page = ScenarioListPage(browser, env)
        scenario_list_page.should_be_scenario_list_page()

    @pytest.mark.test_full_smoke
    @pytest.mark.fast_test
    # @pytest.mark.incremental
    def test_user_can_change_project(self, env, browser):
        scenario_list_page = ScenarioListPage(browser=browser, env=env, language=language)
        scenario_list_page.should_be_scenario_list_page()

        scenario_list_page.should_be_sidebar()
        scenario_list_page.choose_project(DPNames.PROJECT_NAME[project_type])
        scenario_list_page.should_be_scenario_list_page(project_url_path=Pages.SCENARIO_LIST[project_type])

    @pytest.mark.open_scenario_from_scenario_list
    @pytest.mark.test_full_smoke
    @pytest.mark.fast_test
    @pytest.mark.select_test
    # @pytest.mark.incremental
    def test_user_can_open_scenario_page_from_scenario_list(self, env, browser):
        scenario_list_page = ScenarioListPage(browser=browser, env=env, language=language)
        scenario_list_page.should_be_scenario_list_page()
        scenario_list_page.user_can_open_scenario_page_by_click_on_scenario_title('test_select')

    @pytest.mark.create_scenario
    @pytest.mark.test_full_smoke
    def test_user_can_open_create_scenario_page(self, env, browser):
        scenario_list_page = ScenarioListPage(browser=browser, env=env, language=language)
        scenario_list_page.should_be_scenario_list_page()
        scenario_list_page.should_be_open_create_scenario_page_by_click_any_jenius_button()
        # scenario_list_page.should_be_open_create_scenario_page_by_click_on_jenius_button_bottom()
        # scenario_list_page.should_be_open_create_scenario_page_by_click_on_jenius_button_left()
        create_scenario_page = CreateScenarioPage(browser=browser, env=env, language=language)
        create_scenario_page.should_be_create_scenario_page()

    @pytest.mark.create_scenario
    @pytest.mark.test_full_smoke
    def test_user_can_create_scenario_and_open_scenario_page(self, env, browser):
        global scenario_id
        global scenario_title

        create_scenario_page = CreateScenarioPage(browser=browser, env=env, language=language)
        create_scenario_page.should_be_create_scenario_page()
        create_scenario_page.create_scenario()

        scenario_page = BaseScenarioPage(browser=browser, env=env, language=language)
        scenario_page.should_be_scenario_page(project_type=project_type)

        scenario_id = scenario_page.get_scenario_id_from_url()
        scenario_title = scenario_page.get_scenario_title()

    @pytest.mark.test_full_smoke
    @custom_parametrize(data=types,
                        skip=skip,
                        arguments=(
                            'system_file_name',
                            'front_name',
                            'scenario_type',
                            'url_path',
                            'optimization_type'
                        ))
    # @pytest.mark.incremental
    def test_user_can_add_input_file(self, env, browser,
                                     system_file_name,
                                     front_name,
                                     scenario_type,
                                     url_path,
                                     optimization_type):
        input_tab = InputTabOnScenarioPage(browser=browser, env=env, language=language)
        input_tab.should_be_input_tab_on_scenario_page()

        # input_tab.should_be_input_name_in_popover_message_list(front_name)

        file_name = f'{system_file_name}.csv'
        input_tab.upload_the_file(project_type=project_type,
                                  input_file_front_name=front_name,
                                  file_name=file_name,
                                  scenario_type=scenario_type,
                                  url_path=url_path,
                                  optimization_type=optimization_type)

        input_tab.file_should_be_uploaded(front_name, system_file_name=file_name, timeout=30)
        input_tab.should_be_not_input_name_in_popover_message_list(front_name)

        # time.sleep(2)

    @pytest.mark.test_full_smoke
    @pytest.mark.select_test
    # @pytest.mark.incremental
    def test_user_can_open_pfr_tab_from_input_tab(self, env, browser):
        input_tab = InputTabOnScenarioPage(browser=browser, env=env, language=language)
        input_tab.should_be_open_pfr_tab_by_click_on_tab_name()

        pfr_tab = PromoPFRTabOnScenarioPage(browser=browser, env=env, language=language)

        # elems1 = ['NATIONAL KEY ACCOUNT', 'Hypermarket', 'ATAC', 'AUCHAN', 'DC DA!']
        #pfr_tab.choose_data_in_hierarchy_elements_select('select customers')

        # elems2 = ['MODERN', 'MILKS', 'TRADI', 'MILKS']
        #pfr_tab.choose_data_in_hierarchy_elements_select('select products')

        pfr_tab.search_data_in_hierarchy_elements_select('select customers', 'text')

        # pfr_tab.choose_data_in_target_variable_select('select variable', 'NS, Abs')
        # time.sleep(1)
        pfr_tab.input_data_in_target_variable_input('holdout', 'text')

        pfr_tab.choose_data_in_target_variable_select('min/max', 'max')
        pfr_tab.choose_data_in_target_variable_select('select variable', 'NS, Abs')

        time.sleep(5)


