# import time
#
# import pytest
#
# from conftest import custom_parametrize
# from input_files.input_data import InputTypeNameMatch
# from pages.base_scenario_page import BaseScenarioPage
# from pages.create_scenario_page import CreateScenarioPage
# from pages.input_tab_on_scenario_page import InputTabOnScenarioPage
# from pages.login_page import LoginPage
# from pages.pfr_tab_on_scenario_page import PFRTabOnScenarioPage
# from pages.scenario_list_page import ScenarioListPage
# from pages.site_data.credentials import Credentials as Creds
# from pages.site_data.default_params import (ProjectType as Ptype,
#                                             DefaultProjectNames as DPNames)
# from pages.site_data.urls import Links, Pages
#
# project_type = Ptype.TETRIS
# types = {Ptype.PROMO: InputTypeNameMatch.Promo.TYPES,
#          Ptype.RTM: InputTypeNameMatch.RTM.TYPES,
#          Ptype.TETRIS: InputTypeNameMatch.Tetris.TYPES,
#          Ptype.CFR: InputTypeNameMatch.CFR.TYPES}[project_type]
#
# skip = {Ptype.PROMO: {},
#         Ptype.RTM: {},
#         Ptype.TETRIS: {'bom': {'method': 'skipif', 'msg': 'Input is not agreed and not finalized'},
#                        'stop_buyers': {'method': 'xfail', 'msg': 'Bug'}},
#         Ptype.CFR: {}}[project_type]
#
#
# class TestFullSmokePath:
#     @pytest.mark.test_full_smoke
#     def test_user_authorization(self, env, browser):
#         link = Links(env).get('LOGIN_PAGE')
#         login_page = LoginPage(browser, env, link)
#         login_page.open()
#         Creds.auth()
#         login_page.authorize_user(*Creds.auth().values())
#
#     @pytest.mark.test_full_smoke
#     def test_user_can_change_project(self, env, browser):
#         scenario_list_page = ScenarioListPage(browser, env)
#         scenario_list_page.should_be_scenario_list_page()
#
#         scenario_list_page.should_be_sidebar()
#
#         scenario_list_page.choose_project(DPNames.PROJECT_NAME[project_type])
#
#         scenario_list_page.should_be_scenario_list_page(project_url_path=Pages.SCENARIO_LIST[project_type])
#
#     @pytest.mark.open_scenario_from_scenario_list
#     @pytest.mark.test_full_smoke
#     def test_user_can_open_scenario_page_from_scenario_list(self, env, browser):
#         scenario_list_page = ScenarioListPage(browser, env)
#         scenario_list_page.should_be_scenario_list_page()
#         scenario_list_page.user_can_open_scenario_page_by_click_on_scenario_title('Scenario_test_1')
#
#     @pytest.mark.create_scenario
#     @pytest.mark.test_full_smoke
#     def test_user_can_open_create_scenario_page(self, env, browser):
#         scenario_list_page = ScenarioListPage(browser, env)
#         scenario_list_page.should_be_scenario_list_page()
#         scenario_list_page.should_be_open_create_scenario_page_by_click_on_jenius_button_bottom()
#         # scenario_list_page.should_be_open_create_scenario_page_by_click_on_jenius_button_left()
#
#     @pytest.mark.create_scenario
#     @pytest.mark.test_full_smoke
#     def test_user_can_create_scenario_and_open_scenario_page(self, env, browser):
#         create_scenario_page = CreateScenarioPage(browser, env)
#         create_scenario_page.should_be_create_scenario_page()
#         create_scenario_page.create_scenario()
#
#         scenario_page = BaseScenarioPage(browser)
#         scenario_page.should_be_scenario_page(project_type=project_type)
#
#     @pytest.mark.test_full_smoke
#     @custom_parametrize(data=types,
#                         skip=skip,
#                         arguments=('system_file_name', 'front_name', 'scenario_type', 'url_path'))
#     def test_user_can_add_input_file(self, env, browser,
#                                      system_file_name,
#                                      front_name,
#                                      scenario_type,
#                                      url_path):
#         input_tab = InputTabOnScenarioPage(browser)
#         input_tab.should_be_input_tab_on_scenario_page()
#
#         # input_tab.should_be_input_name_in_popover_message_list(front_name)
#
#         file_name = f'{system_file_name}.csv'
#         input_tab.upload_the_file(project_type=project_type,
#                                   input_file_front_name=front_name,
#                                   file_name=file_name,
#                                   scenario_type=scenario_type,
#                                   url_path=url_path)
#
#         input_tab.file_should_be_uploaded(front_name, system_file_name=file_name, timeout=30)
#         input_tab.should_be_not_input_name_in_popover_message_list(front_name)
#
#         # time.sleep(2)
#
#     @pytest.mark.test_full_smoke
#     def test_user_can_open_pfr_tab_from_input_tab(self, env, browser):
#         input_tab = InputTabOnScenarioPage(browser)
#         input_tab.should_be_open_pfr_tab_by_click_on_jenius_button_left()
#
#         # pfr_tab = PFRTabOnScenarioPage(browser)
#         # pfr_tab.should_be_pfr_tab_on_scenario_page()
#
#         time.sleep(2)
