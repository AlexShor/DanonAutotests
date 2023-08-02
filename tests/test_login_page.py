import time

from ..pages.base_scenario_page import BaseScenarioPage
from ..pages.scenario_list_page import ScenarioListPage
from ..pages.create_scenario_page import CreateScenarioPage
from ..pages.input_tab_on_scenario_page import InputTabOnScenarioPage
from ..pages.login_page import LoginPage
from ..pages.site_data.urls import Links
from ..input_files.input_data import InputTypeNameMatch
from pages.site_data.credentials import Credentials as Creds


class TestStart:
    def test_user_authorization(self, env, browser):
        link = Links(env).get('LOGIN_PAGE')
        login_page = LoginPage(browser, env, link)
        login_page.open()
        Creds.auth()
        login_page.authorize_user(*Creds.auth().values())

    def test_user_cen_open_create_scenario_page(self, env, browser):
        link = Links(env).get('SCENARIO_LIST_PAGE')
        scenario_list_page = ScenarioListPage(browser, env, link)
        scenario_list_page.should_be_scenario_list_page()
        scenario_list_page.user_cen_open_create_scenario_page()

    def test_user_cen_create_scenario_and_open_scenario_page(self, env, browser):
        link = Links(env).get('PROMO_CREATE_SCENARIO')
        create_scenario_page = CreateScenarioPage(browser, env, link)
        create_scenario_page.should_be_create_scenario_page()
        create_scenario_page.create_scenario('', '', 'regular scenario', '2023 Q4')

    def test_user_can_add_input_files(self, env, browser):
        scenario_page = BaseScenarioPage(browser)
        scenario_page.should_be_scenario_page()

        input_tab = InputTabOnScenarioPage(browser)
        for file_user_name, file_system_name in InputTypeNameMatch.Promo.TYPES.values():
            #file_path = rf'../input_files/files/promo/input_files/{file_system_name}.csv'
            file_path = rf'C:\Users\LexSh\YandexDisk\Projects\Advanced\Danone\DaneneAutotests\input_files\files\promo\input_files\{file_system_name}.csv'
            input_tab.upload_the_file(file_user_name, file_path)

        time.sleep(2)
