import time

from ..pages.base_scenario_page import BaseScenarioPage
from ..pages.scenario_list_page import ScenarioListPage
from ..pages.create_scenario_page import CreateScenarioPage
from ..pages.login_page import LoginPage
from ..pages.site_data.urls import Links


def test_user_authorization(env, browser, authoriz_creds):
    link = Links(env).get('LOGIN_PAGE')
    login_page = LoginPage(browser, env, link)
    login_page.open()
    login_page.authorize_user(*authoriz_creds.values())

    link = Links(env).get('SCENARIO_LIST_PAGE')
    scenario_list_page = ScenarioListPage(browser, env, link)
    scenario_list_page.should_be_scenario_list_page()
    scenario_list_page.user_cen_open_create_scenario_page()

    link = Links(env).get('PROMO_CREATE_SCENARIO')
    create_scenario_page = CreateScenarioPage(browser, env, link)
    create_scenario_page.should_be_create_scenario_page()
    create_scenario_page.create_scenario('', '', 'regular scenario', '2023 Q4')
    scenario_id = create_scenario_page.get_scenario_id_from_url()

    link = Links(env).get('SCENARIO_PAGE', scenario_id)
    scenario_page = BaseScenarioPage(browser, env, link)
    scenario_page.should_be_scenario_page()

    time.sleep(2)
